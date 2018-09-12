# Processing PDF

This repo contains a **prototype** algorithm for the QGIS processing framework allowing to export PDFs.

It works by taking following inputs :
- a *QGIS project* (current project if nothing specified)
- the *layout name* (the layout that you want to output)
- a list of *template layers* (layers from the project that are to be replaced - as a comma separated list of layers ids)
- a list of *override layers* (layers that will replace the template layers - must match the count and order)
- an *output folder* (the place where outputs will be stored)

## Installation

Install as a QGIS python plugin.

This requires QGIS 3.3 including with following patch (not merged yet) : https://github.com/qgis/QGIS/pull/7864

## Usage

Run (or batch run) the new `Export to PDF` algorithm.

## Sample project

A sample project containing a processing model that uses the PDF exporter is included.

To use, open the project in QGIS 3.3, and run the `RiskTools/Flood on buildings` algorithm. Use the buildings layer and one of the rasters from the data folder as inputs. You can run it in batch.

## Known issues

- Issue when running the sample in batch mode because of https://issues.qgis.org/issues/19836

## Roadmap

Prototype :

- Support other type of exports (atlas, image, ...)
- Allow to define some variables to be used in the composer (for example to display a scenario name)
- Explore using layouts files (.qpt) instead of QgsProjects, would probably require some "project builders" helper algorithms
- See if/how we can embed project files in processing models, to provide "self contained" PDF generators
- See if it's possible to use the custom widgets in the graphical modeler too
- ...

Long term:

- see if the concept can be enlarged so that `Export as PDF` becomes just be one of several other helper algorithms (such as append/prepend/override layer, add layouts, export PDF, etc.), which probably would require having a new QGIS project parameter type in processing
- bring this in QGIS core (as python)
- once stabilized, eventually port to C++
- ...

## References

See discussion on the mailing list : https://lists.osgeo.org/pipermail/qgis-developer/2018-September/054424.html
