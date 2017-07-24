---
layout: kbase_article
title: Guide to image labeling
---



# CAM2 Image Labeling Guidelines
 This document is a guide for how to label images.  It is mostly copied from the PASCAL VOC2007 image labeling guidelines.  
 
### What to label
All objects of the defined categories, unless:
- you are unsure what the object is.
- the object is very small (at your discretion).
- less than 10-20% of the object is visible.
If this is not possible because too many objects, mark image as bad.

### Viewpoint
Record the viewpoint of the ‘bulk’ of the object e.g. the body rather than the head.  Allow viewpoints within 10-20 degrees.
If ambiguous, leave as ‘Unspecified’.

### Bounding box
Mark the bounding box of the visible area of the object (not the estimated total extent of the object).
Bounding box should contain all visible pixels, except where the bounding box would have to be made excessively large to include a few additional pixels (<5%) e.g. a car aerial.
### Occlusion/ truncation
If more than 15-20% of the object is occluded and lies outside the bounding box, mark as ‘Truncated’.
Do not mark as truncated if the occluded area lies within the bounding box.
### Image quality/ illumination
Images which are poor quality (e.g. excessive motion blur) should be marked bad.  However, poor illumination (e.g. objects in silhouette) should not count as poor quality unless objects cannot be recognised.
Images made up of multiple images (e.g. collages).
### Clothing/mud/ snow etc.
If an object is ‘occluded’ by a close-fitting occluder e.g. clothing, mud, snow etc., then the occluder should be treated as part of the object.
### Transparency
Do label objects visible through glass, but treat reflections on the glass as occlusion.
### Mirrors
Do label objects in mirrors.
### Pictures
Label objects in pictures/posters/signs only if they are photorealistic but not if cartoons, symbols etc.


## Guidelines on categorisation
Bicycle:
   Includes tricycles, unicycles

Boat:
   Ships, rowing boats, pedaloes but not jet skis

Bus:
   Includes minibus

Car:
   Includes cars, vans, people carriers etc.  
   Do not label where only the vehicle interior is shown.

Motorbike:
   Includes mopeds, scooters, sidecars

Train:
   Includes train carriages, excludes trams


