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

Vendored third party designs.


h10_resource
------------

The h10_resource tier is intended for the
management of static resources used across
all products and product lines.

This includes things like brand logo and
pallette, document templates, organisation
level registers and mini-databases, and
anything else with a similar organisation
wide pattern of use.


h20_capability
--------------

The h20_capability tier is intended for the
management of design elements which are used
across multiple products and product lines.

This includes things like proprietary software
component libraries, APIs, middleware and design
kits.


h30_product
-----------

The h30_product tier is intended for the
management of designs of off the shelf
products.

The designs in the h30_product tier are
normally composed of design elements drawn
from the h20_capability tier.


h40_bespoke
-----------

The h40_bespoke tier is intended for the
management of designs of bespoke products.

The designs in the h40_bespoke tier are
normally composed of tailorings applied
on top of off the shelf product designs
drawn from the h30_product tier.


h50_research
------------

The h50_research tier is intended for the
management of design elements that arise
from research activities.

The design elements managed in the h50_research
tier are normally composed of tailorings and
improvements that modify or replace design
elements drawn from previous tiers.


h60_demo
--------

The h60_demo tier is intended for the
management of design elements that arise
from the preparation of technical
demonstrations or early feasibility studies.

The design elements managed in the h50_research
tier are normally composed of tailorings and
improvements that modify or replace design
elements drawn from previous tiers.


h70_internal
------------

The h70_internal tier is intended for the
management of design elements, programs,
scripts, tools and utilities that are
used to automate the design process itself.