=================================
Source design document repository
=================================


Overview
========

This directory is used as the main repository
for design documents.

This acts as the source of truth for system
design configurations and the input to
any manufacturing, production or commissioning
process.


Structure
=========

h00_thirdparty
--------------

The h00_thirdparty tier is intended for design
elements which are brought in from third parties
and modified or customised by us in some way.

Most third party dependencies will reside outside
of the hierarchy and be incorporated into one or
more managed environments, but in some cases we
need to tailor or adapt those dependencies in
some way, which means co-versioning them and
managing them alongside our internally developed
design elements.

In principle, third party design elements should
not depend on nor know about any internally
developed design element.


h10_resource
------------

The h10_resource tier is intended for the
management of static resources used across all
products and product lines.

This includes things like brand logo and pallette,
document templates, organisation level registers
and mini-databases, and anything else with a
similar organisation wide pattern of use.


h20_functionality
-----------------

The h20_functionality tier is intended for the
management of design elements which are intended
for generic reuse.

This includes things like software libraries,
APIs and other similar design elements.

Most of the detailed design work should sit at
this level of the hierarchy.


h30_platform
------------

The h30_platform tier is intended for the
management of design elements which are intended
for use as an enabling platform of some sort.

This includes things like software frameworks
and middleware.

It is expected that design elements at the
platform level will make use of detailed design
elements managed at the h20_functionality level
of the hierarchy.


h40_component
-------------

The h40_component tier is intended for the
management of design elements which are intended
for reuse within the context of a component
framework.

It is expected that design elements at the
component level will make use of detailed design
elements managed at the h20_functionality level
of the hierarchy as well as frameworks managed
at the h30_platform level.


h50_product
-----------

The h50_product tier is intended for the
management of the design of each of our
'off-the-shelf' product lines.

It is expected that designs at the h50_product
tier will consist primarily of configuration
data that assembles components defined at the
h40_component tier into the functional chains
that support the feature mix of each specific
product line.

Some small quantity of detailed design work is
also acceptable here, but the majority of the
design effort should be concentrated in the
lower levels of the hierarchy where the costs
may be more readily amortized across multiple
product lines.


h60_bespoke
-----------

The h60_bespoke tier is intended for the
management of designs of bespoke products.

The designs in the h60_bespoke tier are
normally composed of tailorings applied
on top of off the shelf product designs
drawn from the h50_product tier.


h70_research
------------

The h70_research tier is intended for the
management of design elements that arise
from research activities.

The design elements managed in the h70_research
tier are normally composed of tailorings and
improvements that modify or replace design
elements drawn from tiers at lower levels of
the hierarchy.


h80_demonstration
-----------------

The h80_demonstration tier is intended for
the management of design elements that arise
from the preparation of technical
demonstrations or early feasibility studies.


h90_internal
------------

The h90_internal tier is intended for the
management of design elements, programs,
scripts, tools and utilities that are
used to automate the design process itself,
along with internal documentation and processes.