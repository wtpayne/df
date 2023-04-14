import json
from fuzzywuzzy import fuzz
from multiprocessing import Pool
import time
import igraph as ig
from pwiki.wiki import Wiki
from pwiki.mquery import MQuery
import re # regex
import argparse

parser = argparse.ArgumentParser(
                    prog = 'Wiki Graph Downloader',
                    description = 'It creates a graph of nodes using the Wikipedia api')
parser.add_argument('-a', '--articles', nargs='+', default=[])
parser.add_argument('-d', '--depth')      # recursive depth
parser.add_argument('-t', '--threshold')      # link frequency threshold for recursive search
parser.add_argument('-n', '--max_links_to_follow')      # Max links to follow

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def get_section_titles(page_text):
    section_titles = re.findall(r'=[a-zA-Z0-9_ ]+==', page_text)
    section_titles = [ title[1:-2] for title in section_titles]
    return section_titles

def get_section_text(page_text, section_title, next_section_title):
    
    startStr = "=" + section_title + "=="
    endStr = "=" + next_section_title + "=="
    start = page_text.find(startStr) + len(startStr)
    end = page_text.find(endStr)
    return page_text[start:end].lower()

def get_summary(page_text, page_title):
    '''
    Gets the first two sentences of the wikipedia article
    '''
    startStr = "{{" + page_title + "}}"

    start = page_text.find(startStr) + len(startStr)
    end = find_nth(page_text,".",2)

    return page_text[start:end].lower()

def vertex_exists(all_vertices, vertex_title):
    for vertex in all_vertices:
        if vertex['id'] == vertex_title:
            return True
    
    return False

def find_vertex_index(all_vertices, vertex_title):
    for index, vertex in enumerate(all_vertices):
        if vertex['id'] == vertex_title:
            return index
    return -1

def add_vertex(all_vertices, vertex_title, vertex_type, overide=False):
    
    if overide:
        index = find_vertex_index(all_vertices, vertex_title)

        # If we find that it already exists, unless it is of higher type
        if index != -1 and all_vertices[index]['type'] != 'page':
            all_vertices[index] = {'id':vertex_title, 'name':vertex_title,'type':vertex_type}
            return all_vertices            

    if not vertex_exists(all_vertices, vertex_title):
        all_vertices.append({'id':vertex_title,'name':vertex_title,'type':vertex_type})

    return all_vertices

def add_edges(all_edges, vertex_title, edges, weights):

    for edge, weight in zip(edges,weights):
        all_edges.append({'source':vertex_title, 'target':edge, 'value':weight})

    return all_edges

def create_section_graph(all_vertices, all_edges, root_title, page_links, page_text):
    '''
    Creates a graph using all the sections 
    '''
    print("Adding section graph for", root_title)
    add_vertex(all_vertices, root_title, 'page', overide=True)

    # Filter links by what appears on specific section
    section_titles = get_section_titles(page_text)

    # section_titles_sorted = sort_links_by_frequency(section_titles, page_text)
    # section_titles_sorted_filtered = filter_low_frequency_links(section_titles_sorted, 10)[:10-1]

    # print("Section titles:", section_titles)

    # for each section, check if a link exists
    for index in range(len(section_titles)-1):

        add_vertex(all_vertices,
                    root_title + ":" + section_titles[index], 
                    'section')
        add_edges(all_edges, root_title + ":" + section_titles[index], [root_title], [1])

        # Get section text and search for links
        section_text = get_section_text(page_text, section_titles[index], section_titles[index+1])    
        
        for link_title in page_links:
            # If there is a link match, append the graph with the link title
            if fuzz.token_set_ratio(section_text, link_title) > 98:
                add_vertex(all_vertices, link_title, 'link')
                add_edges(all_edges, root_title + ":" + section_titles[index], [link_title], [0.1])

    return all_vertices, root_title

def request_pages_text(wiki, pages):
    '''
    Gets all the text of all the wikipedia pages specified as a bulk request to save on bandwidth
    '''
    print("Requesting ", len(pages), "pages from Wikipedia API.")
    response = MQuery.page_text(wiki,pages)
    return response

def extract_summary_links(page_links, page_text, root_title):
    '''
    Creates a list of all the links listed in the summary of the provided page
    '''

    # Filter links by what appears on the summary
    summary = get_summary(page_text, root_title)
    summary_links = []
    for link_title in page_links:
        if fuzz.token_set_ratio(summary,link_title) > 98:
            summary_links.append(link_title)
    return summary_links        

def sort_links_by_frequency(links, text):
    
    link_frequency = []
    for link in links:
        link_frequency.append(text.lower().count(link.lower()))

    zipped = zip(link_frequency, links)
    sorted_zipped = sorted(zipped, key = lambda x: x[0], reverse=True)

    return sorted_zipped

def filter_low_frequency_links(root_page_links_sorted, threshold):
    
    filtered_links = []
    for frequency, link in root_page_links_sorted:
        if frequency > threshold:
            filtered_links.append(link)
    
    return filtered_links

def merge_processes(all_vertices, all_edges, new_vertices, new_edges):

    for element in new_vertices:
        add_vertex(all_vertices, element['id'], element['type'], overide=True)

    for element in new_edges:
        all_edges.append(element)


def generate_graph_dict(wiki, root_page_text, root_page_title, all_vertices, all_edges, recursion_depth=0, MAX_DEPTH=2, frequency_threshold=3, max_links_to_follow=4):

    # Get root page links
    root_page_links = wiki.links_on_page(root_page_title)

    # Add links and root page into dictionary to make graph later
    create_section_graph(all_vertices, all_edges, root_page_title, root_page_links, root_page_text)

    # Calculate how many times a certain link is mentioned in a page, sort, and filter using frequency_threshold
    root_page_links_sorted = sort_links_by_frequency(root_page_links, root_page_text)
    root_page_links_sorted_filtered = filter_low_frequency_links(root_page_links_sorted, frequency_threshold)[:max_links_to_follow-1]

    # Print stats
    print("\n")
    print("Depth:", recursion_depth, "-"*recursion_depth, "| Page Title:", root_page_title)
    print("Depth:", recursion_depth, "-"*recursion_depth, "| Number of filtered links:", len(root_page_links_sorted_filtered))
    print("Depth:", recursion_depth, "-"*recursion_depth, "| Filtered links:", root_page_links_sorted_filtered)

    # For each of the new links added to the graph, recurse
    if recursion_depth+1 <= MAX_DEPTH:
        print("Depth:", recursion_depth,"-"*recursion_depth, "| GOING DEEPER")

        link_pages_text = request_pages_text(wiki, root_page_links_sorted_filtered)

        for link_title in root_page_links_sorted_filtered:
            all_vertices, all_edges = generate_graph_dict(wiki, link_pages_text[link_title], link_title, all_vertices, all_edges, recursion_depth+1, MAX_DEPTH, frequency_threshold)      
    
    else:
        print("Depth:", recursion_depth,"-"*recursion_depth,"| REACHED MAX DEPTH")
    
    return all_vertices, all_edges

def save_graph(all_vertices, all_edges, articles_list):

    outfile_name = ''.join([article_name + "_" for article_name in articles_list])
    print("Saving to file:", outfile_name)

    # Save json
    jsonString = json.dumps({'nodes':all_vertices, 'links':all_edges}, indent=2)
    jsonFile = open("output/"+outfile_name + ".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    # Save graphml
    g = ig.Graph.DictList(all_vertices, all_edges)
    print(g.summary(verbosity=0))
    g.write_graphml("output/"+outfile_name + ".graphml")

def main(args):

    articles_list = args.articles
    depth = int(args.depth)
    threshold = int(args.threshold)
    max_links_to_follow = int(args.max_links_to_follow)

    # Create new Wiki instance, pointed to en.wikipedia.org, not logged in
    wiki = Wiki()
    all_vertices = []
    all_edges = []

    for root_page_title in articles_list:

        # Get the text of the root page
        root_page_text = request_pages_text(wiki, [root_page_title])[root_page_title]

        # Get root page links
        root_page_links = wiki.links_on_page(root_page_title)

        # Add links and root page into dictionary to make graph later
        create_section_graph(all_vertices, all_edges, root_page_title, root_page_links, root_page_text)

        # Calculate how many times a certain link is mentioned in a page, sort, and filter using threshold
        root_page_links_sorted = sort_links_by_frequency(root_page_links, root_page_text)
        root_page_links_sorted_filtered = filter_low_frequency_links(root_page_links_sorted, threshold)[:max_links_to_follow-1]

        print("\n")
        print("Depth:", 0, "| Page Title:", root_page_title)
        print("Depth:", 0, "| Number of filtered links:", len(root_page_links_sorted_filtered))
        print("Depth:", 0, "| Filtered links:", root_page_links_sorted_filtered)

        # # Get all the links that appear in the summary of the root page
        # root_summary_links = extract_summary_links(root_page_links, root_page_text, root_page_title)
        # print("Root Summary Links: ",root_summary_links)

        # Get the text of all the pages linked in the summary of the root page
        link_pages_text = request_pages_text(wiki, root_page_links_sorted_filtered)

        print("--- ROOT GRAPH", "#vertices:", len(all_vertices), "#edges:", len(all_edges))
        # Process text of linked pages recursively, the first level of recursion using multiprocessing
        if depth > 0:
            with Pool(4) as pool:
                for new_vertices, new_edges in pool.starmap(generate_graph_dict, 
                    [(wiki, link_pages_text[child_title], child_title, all_vertices, all_edges, 1, depth, threshold) for child_title in link_pages_text]):
                    merge_processes(all_vertices, all_edges, new_vertices, new_edges)
                    print("--- UPDATING GRAPH", "#vertices:", len(all_vertices), "#edges:", len(all_edges))

    save_graph(all_vertices, all_edges, articles_list)

if __name__ == '__main__':

    args = parser.parse_args()
    start_time = time.time()
    main(args)
    print("--- %s seconds ---" % (time.time() - start_time))