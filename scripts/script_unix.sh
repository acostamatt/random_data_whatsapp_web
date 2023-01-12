#!/bin/bash
mkdir -p ../src/views/base

pyside6-uic ../ui/sorteo_base.ui -o ../src/views/base/sorteo_base.py
pyside6-uic ../ui/table_view_sorteo.ui -o ../src/views/base/table_view_sorteo.py