# Gem5 Lab2

## Screenshots of hardware configuration result 

### private_l1_private_l2_cache_hierarchy
* using two cores
* single_tile

    <img src="Images/single_tile_Lab447PrivateL1PrivateL2CacheHierarchy/single_tile_Lab447PrivateL1PrivateL2CacheHierarchy.png" width = "75%" height = "60%">

* multi_tile
<br/>

    <img src="Images/multi_tile_Lab447PrivateL1PrivateL2CacheHierarchy/multi_tile_Lab447PrivateL1PrivateL2CacheHierarchy.png" width = "75%" height = "60%">

### private_l1_shared_l2_cache_hierarchy 
* using two cores
* single_tile

    <img src="Images/single_tile_Lab447PrivateL1SharedL2CacheHierarchy/single_tile_Lab447PrivateL1SharedL2CacheHierarchy.png" width = "75%" height = "60%">

* multi_tile

    <img src="Images/multi_tile_Lab447PrivateL1SharedL2CacheHierarchy/multi_tile_Lab447PrivateL1SharedL2CacheHierarchy.png" width = "75%" height = "60%">

## Screenshots of stats, anything that could prove it works 

### private_l1_private_l2_cache_hierarchy

* single_tile

    <img src="Images/single_tile_Lab447PrivateL1PrivateL2CacheHierarchy/work.png" width = "85%" height = "70%">

* multi_tile

    <img src="Images/multi_tile_Lab447PrivateL1PrivateL2CacheHierarchy/work.png" width = "85%" height = "70%">

### private_l1_shared_l2_cache_hierarchy 

* single_tile

    <img src="Images/single_tile_Lab447PrivateL1SharedL2CacheHierarchy/work.png" width = "85%" height = "70%">

* multi_tile

    <img src="Images/multi_tile_Lab447PrivateL1SharedL2CacheHierarchy/work.png" width = "85%" height = "70%">

## Brief description of your implementation of function

### schematic diagram

<img src="Images/Connection_Between_Two_Components.png" width = "55%" height = "40%">

### private_l1_private_l2_cache_hierarchy
* each L1 cache corresponds to its own L2 cache

* define components
<br/>

  <img src="Images/privateL2_code.png" width = "55%" height = "40%">


* wiring
<br/>

  <img src="Images/privateL2_wiring.png" width = "55%" height = "40%" style = "left: 10%">


### private_l1_shared_l2_cache_hierarchy 
* each L1 cache corresponds to same L2 cache

* define components
<br/>

  <img src="Images/shareL2_code.png" width = "65%" height = "50%">

* wiring
<br/>

   <img src="Images/shareL2_wiring.png" width = "55%" height = "40%" style = "left: 10%">
