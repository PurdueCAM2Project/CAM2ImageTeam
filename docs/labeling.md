<link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet"> 
<div markdown="1" style="font-family: 'Ubuntu', sans-serif">

[<<< Back to Image Team knowledge base home](index)

[//]: # (YOUR MARKDOWN CODE STARTS BELOW THIS LINE!!!)




# CAM2 Image Labeling Guidelines :woman::man:
 This document is a guide for how to label images.  It is mostly copied from the PASCAL VOC2007 image labeling guidelines.  
 
### What to label

Label as much as possible! If you reasonably think it is a person, the mark the pixels as a person. While we are only marking people, there are some subsets of people we are interesting in marking:

1. "person": 60% - 100% visible
2. "occluded_person": 40% - 60% visible
3. "partial_person": 20% - 40%

Don't label if:
- you are unsure what the object is.
- less than 10-20% of the object is visible.

Our goal is variety! Label *everyone* in a crowd if there is one. Use images with poor lighting. While we don't want to purposefully seek out poor images, we want the dataset to be *representative* of the network camera data.

### Viewpoint
Record the viewpoint of the ‘bulk’ of the object e.g. the body rather than the head.  Allow viewpoints within 10-20 degrees.
If ambiguous, leave as ‘Unspecified’.

### Bounding box
Mark the bounding box of the visible area of the object (not the estimated total extent of the object).
Bounding box should contain all visible pixels, except where the bounding box would have to be made excessively large to include a few additional pixels (<5%) e.g. a car aerial.

### Occlusion/ truncation
If more than 15-20% of the object is occluded and lies outside the bounding box, mark as ‘Truncated’ in addition to the labels above.
Do not mark as truncated if the occluded area lies within the bounding box.

### Image quality/ illumination
Images which are poor quality (e.g. excessive motion blur) should **not** be marked bad. However, poor illumination (e.g. objects in silhouette) should not count as poor quality unless objects cannot be recognised. We want a *representative* sample.


### Clothing/mud/ snow etc.
If an object is ‘occluded’ by a close-fitting occluder e.g. clothing, mud, snow etc., then the occluder should be treated as part of the object.

### Transparency
Do label objects visible through glass, but treat reflections on the glass as occlusion.

### Mirrors
Do label objects in mirrors.

### Pictures
Label objects in pictures/posters/signs only if they are photorealistic but not if cartoons, symbols etc.

## Guidelines on categorisation
A "person" counts as anything you can recognize as a person. We are not concerned with the limits of image processing, but rather getting a representative sample of network camera data.




[//]: # (YOUR MARKDOWN CODE ENDS ABOVE THIS LINE!!!)

</div>