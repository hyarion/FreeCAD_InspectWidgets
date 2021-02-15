## FreeCAD Inspect Widgets Addon
Inspect widgets in FreeCAD

![Inspect-Widget-Addon](https://user-images.githubusercontent.com/4140247/107982828-b8b96c00-6f92-11eb-9c38-b7b13330042d.png)

## Description

This addon will expose the qss path to elements in the Qt interface. This helps stylesheet creators find the right selectors to modify in stylesheets in order to customize the UI.

## Background

A request was made in the FreeCAD community to have a sort of Chrome dev tools but for Qt. This addon was created in response.

## Installation

* Open a terminal
  ```
  cd ~/.FreeCAD/Mod
  git clone https://github.com/hyarion/FreeCAD_InspectWidgets
  ```
* Restart FreeCAD  
* Activate via `View > Panels > Inspect Widgets`  

## Usage 

* Make sure  `View > Panels > Inspect Widgets` is activated
* An 'Inspect Widgets' panel will be visible in the task panel.  
* Press `Inspect` button
Result: the qss path will be dynamically update under the panel everytime the mouse hovers over an aspect of the interface

## Developer

[@hyarian](https://github.com/hyarion/)

## Licence
