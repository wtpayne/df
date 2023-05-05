# -*- coding: utf-8 -*-
"""
Planner prototype command line interface logic.

"""


import collections
import datetime
import math
import os.path

import da.timebox

import bunch
import openpyxl
import openpyxl.styles
import openpyxl.styles.borders


# First column = tiny.
# First row = tiny.
# Row headings.
#

# -----------------------------------------------------------------------------
def run(filepath_out):
    """
    Generate the spreadsheet.

    """
    workbook        = openpyxl.Workbook()
    worksheet       = workbook.active
    worksheet.title = 'Schedule'
    style           = _get_style_palette()

    num_rows        = 80
    num_columns     = 200

    _set_background_style(
            worksheet, style, num_rows, num_columns)


    date_start   = datetime.datetime(year   = 2017,
                                     month  = 1,
                                     day    = 1)

    date_end     = datetime.datetime(year   = 2018,
                                     month  = 12,
                                     day    = 24)

    row_start    = 2
    column_start = 2
    row_end      = 80

    _write_calendar(worksheet,
                    style,
                    row_start,
                    row_end,
                    column_start,
                    date_start,
                    date_end)

    # Column width.
    #
    _set_column_width(worksheet, idx = 0, width = 1)
    _set_column_width(worksheet, idx = 1, width = 20)
    for idx in range(2, num_columns):
        _set_column_width(worksheet, idx, width = 3)

    workbook.save(filepath_out)


# -----------------------------------------------------------------------------
def _set_column_width(worksheet, idx, width):
    """
    Set the width of the specified column.

    Column *must* exist already.

    """
    column_letter = tuple(worksheet.column_dimensions.keys())[idx]
    worksheet.column_dimensions[column_letter] = \
        openpyxl.worksheet.dimensions.ColumnDimension(
            worksheet,
            index = column_letter,
            width = width)


# -----------------------------------------------------------------------------
def _write_calendar(worksheet,
                    style,
                    row_start,
                    row_end,
                    column_start,
                    date_start,
                    date_end):
    """
    Write all header cells.

    """
    row_year               = row_start + 0
    row_quarter            = row_start + 1
    row_month              = row_start + 2
    row_timebox            = row_start + 3
    row_week               = row_start + 4

    ws = worksheet
    _write_header_cell(ws, style, row_year,    column_start, 'year')
    _write_header_cell(ws, style, row_quarter, column_start, 'quarter')
    _write_header_cell(ws, style, row_month,   column_start, 'month')
    _write_header_cell(ws, style, row_timebox, column_start, 'timebox')
    _write_header_cell(ws, style, row_week,    column_start, 'iso2604 week')


    map_year_to_column     = collections.defaultdict(set)
    map_quarter_to_column  = collections.defaultdict(set)
    map_month_to_column    = collections.defaultdict(set)
    map_timebox_to_column  = collections.defaultdict(set)


    for (idx, date_data) in enumerate(_iter_date_data(date_start, date_end)):

        (year, quarter, month, timebox, week) = date_data
        column = column_start + idx + 1

        quarter_id = year + quarter
        month_id   = quarter_id + month

        map_year_to_column[year].add(column)
        map_quarter_to_column[quarter_id].add(column)
        map_month_to_column[month_id].add(column)
        map_timebox_to_column[timebox].add(column)

        _write_header_cell(worksheet, style, row_year,    column, year)
        _write_header_cell(worksheet, style, row_quarter, column, quarter)
        _write_header_cell(worksheet, style, row_month,   column, month)
        _write_header_cell(worksheet, style, row_timebox, column, timebox)
        _write_header_cell(worksheet, style, row_week,    column, week)

        if timebox.endswith('A'):
            _highlight_column(worksheet,
                              style,
                              row_start = row_timebox,
                              row_end   = row_end,
                              column    = column)

    _merge_columns(worksheet, row_year,     map_year_to_column)
    _merge_columns(worksheet, row_quarter,  map_quarter_to_column)
    _merge_columns(worksheet, row_month,    map_month_to_column)
    _merge_columns(worksheet, row_timebox,  map_timebox_to_column)


# -----------------------------------------------------------------------------
def _highlight_column(worksheet, style, row_start, row_end, column):
    """
    """
    for row in range(row_start, row_end + 1):
        cell      = worksheet.cell(row    = row,
                                   column = column)
        cell.fill = style.fill.mild
        cell.font = style.font.medium


# -----------------------------------------------------------------------------
def _write_header_cell(worksheet, style, row, column, value):
    """
    Write the specified header cell.

    """
    cell            = worksheet.cell(row = row, column = column)
    cell.value      = value
    cell.border     = style.border.header
    cell.alignment  = style.alignment.header


# -----------------------------------------------------------------------------
def _merge_columns(worksheet, row, map_to_column):
    """
    Merge columns according to the specified map of group_id to set_of_columns.

    """
    for set_of_columns in map_to_column.values():
        worksheet.merge_cells(start_row    = row,
                              end_row      = row,
                              start_column = min(set_of_columns),
                              end_column   = max(set_of_columns))


# -----------------------------------------------------------------------------
def _iter_date_data(date_start, date_end):
    """
    Yield data for the date header.

    """
    for date in _iter_thursdays(date_start, date_end):

        (iso_year, iso_week, _) = date.isocalendar()

        timebox            = da.timebox.ident(date)
        timebox_month      = int(timebox[2:4])
        idx_month          = timebox_month - 1
        months_per_year    = 12
        proportion_of_year = idx_month / months_per_year
        quarters_per_year  = 4
        float_quarter      = 1 + (proportion_of_year * quarters_per_year)
        int_quarter        = math.floor(float_quarter)
        month_names        = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

        year    = str(iso_year)
        quarter = 'Q' + str(int_quarter)
        month   = month_names[timebox_month - 1]
        week    = str(iso_week)

        yield (year, quarter, month, timebox, week)


# -----------------------------------------------------------------------------
def _iter_thursdays(date_start, date_end):
    """
    Yield one day per week for the specified dates (inclusive).

    """
    days_in_week = 7
    one_week     = datetime.timedelta(days = days_in_week)
    thurs_start  = da.day.thursday_week_of_the(date_start)
    thurs_end    = da.day.thursday_week_of_the(date_end)

    date = thurs_start
    while date < thurs_end:
        date = date + one_week
        yield (date)


# -----------------------------------------------------------------------------
def _set_background_style(worksheet, style, num_rows, num_columns):
    """
    Set default style (solid background colour fill) for the specified cells.

    """
    for idx_row in range(num_rows):
        for idx_column in range(num_columns):

            cell      = worksheet.cell(row    = idx_row + 1,
                                       column = idx_column + 1)
            cell.fill = style.fill.medium
            cell.font = style.font.medium


# -----------------------------------------------------------------------------
def _get_style_palette():
    """
    Return a Bunch of openpyxl styles.

    """
    style           = bunch.Bunch()
    style.rgb       = bunch.Bunch()
    style.fill      = bunch.Bunch()
    style.side      = bunch.Bunch()
    style.font      = bunch.Bunch()
    style.border    = bunch.Bunch()
    style.alignment = bunch.Bunch()

    # Define colour names.
    #
    style.rgb.pure_white    = 'FFFFFF'
    style.rgb.off_white     = 'F5F5F5'
    style.rgb.light_grey    = 'EEEEEE'
    style.rgb.mid_grey      = 'CCCCCC'
    style.rgb.dark_grey     = '303030'
    style.rgb.off_black     = '202020'
    style.rgb.pure_black    = '000000'
    style.rgb.red           = 'FF0000'
    style.rgb.green         = '00FF00'
    style.rgb.blue          = '0000FF'

    # Define colour roles.
    #
    style.rgb.bg_strong     = style.rgb.pure_white
    style.rgb.bg_medium     = style.rgb.off_white
    style.rgb.bg_mild       = style.rgb.light_grey
    style.rgb.medium        = style.rgb.mid_grey
    style.rgb.fg_mild       = style.rgb.dark_grey
    style.rgb.fg_medium     = style.rgb.off_black
    style.rgb.fg_strong     = style.rgb.pure_black
    style.rgb.accent_a      = style.rgb.red
    style.rgb.accent_b      = style.rgb.green
    style.rgb.accent_c      = style.rgb.blue
    style.rgb.accent_d      = style.rgb.red
    style.rgb.accent_e      = style.rgb.green
    style.rgb.accent_f      = style.rgb.blue

    # Define solid fills.
    #
    style.fill.strong       = _fill(style.rgb.bg_strong)
    style.fill.medium       = _fill(style.rgb.bg_medium)
    style.fill.mild         = _fill(style.rgb.bg_mild)
    style.fill.accent_a     = _fill(style.rgb.accent_a)
    style.fill.accent_b     = _fill(style.rgb.accent_b)
    style.fill.accent_c     = _fill(style.rgb.accent_c)
    style.fill.accent_d     = _fill(style.rgb.accent_d)
    style.fill.accent_e     = _fill(style.rgb.accent_e)
    style.fill.accent_f     = _fill(style.rgb.accent_f)

    # Define sides.
    #
    style.side.medium       = _side(style.rgb.medium)

    # Define fonts.
    #
    style.font.mild         = _font(style.rgb.fg_mild)
    style.font.medium       = _font(style.rgb.fg_medium)
    style.font.strong       = _font(style.rgb.fg_strong)

    # Define borders.
    #
    style.border.header     = _border('nsew', style.side.medium)

    # Define alignments.
    #
    style.alignment.header  = _alignment('bottom', 'center')
    style.alignment.body    = _alignment('center', 'center')

    return style


# -----------------------------------------------------------------------------
def _alignment(vertical, horizontal):
    """
    Return an openpyxl.styles.Alignment object.

    """
    return openpyxl.styles.Alignment(
                        horizontal    = horizontal,
                        vertical      = vertical,
                        text_rotation = 0,
                        wrap_text     = False,
                        shrink_to_fit = False,
                        indent        = 0)


# -----------------------------------------------------------------------------
def _border(direction_string, style):
    """
    Return a openpyxl.styles.borders.Border object.

    """
    direction_to_side_mapping = {
        'n':    'top',
        's':    'bottom',
        'e':    'right',
        'w':    'left'
    }
    params           = dict()
    direction_string = direction_string.lower()
    for direction_char, side in direction_to_side_mapping.items():
        if direction_char in direction_string:
            params[side] = style
    return openpyxl.styles.borders.Border(**params)


# -----------------------------------------------------------------------------
def _side(rgb):
    """
    Return a openpyxl.styles.Side object with the specified colour set.

    """
    return openpyxl.styles.borders.Side(border_style = 'thin',
                                        color        = rgb)


# -----------------------------------------------------------------------------
def _font(rgb):
    """
    Return an openpyxl.styles.Font object with the specified colour set.

    """
    return openpyxl.styles.Font(name      = 'Roboto Light',
                                size      = 10.5,
                                color     = rgb)


# -----------------------------------------------------------------------------
def _fill(rgb):
    """
    Return a openpyxl.styles.PatternFill object with one solid colour set.

    """
    return openpyxl.styles.PatternFill(fill_type   = 'solid',
                                       start_color = rgb,
                                       end_color   = rgb)
