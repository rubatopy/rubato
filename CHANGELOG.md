# Changelog

## [Unreleased]

### Breaking Changes

-   `Polygon`s MUST take in a list of vectors in clockwise order instead of counter-clockwise as was before. Generator methods
    automatically reflect this change but if you are passing in your own lists, make sure to reflect this change.
-   `component.true_z()` is now a function instead of a property method. This is to match with our new property method
    convention.

### Added

-   `gameobject.remove_ind()` method to remove an individual component from a game object with a given index.
    Use this to remove components from a game object which holds multiple instances of the same type of component.
-   `component.true_pos()` and `component.true_rotation()` methods to get the position and rotation of a component in
    world space. These functions correctly apply the gameobjects position and rotation to the component while respecting
    offsets.
-   `Vector.poly()` and `Vector.rect()` methods to generate lists of vertices for regular polygons and rectangles.
-   `color.clone()`.
-   Functions that required Vectors before now accept appropriately-sized tuples.
-   `Events.MOUSEWHEEL` and `Events.SCROLL` (which are the same), propagating mouse scroll events.
-   `GameObject`s and `Group`s can now be hidden in order to make their children not draw.
-   `GameObjects`s can be active just like groups.
-   Allowing passing in the hidden attribute into `Component` constructors.

### Changed

-   Modified the internal workings of `gameobject`s components data structure to more more flexibly handle inputs.
    (Can now handle getting components by a parent type (such as Hitbox or Component or even object)).
-   Renamed `vector.distance_between()` to `vector.dist_to()`.
-   Renamed `polygon.translated_verts()` to `polygon.offset_verts()`.
-   Renamed `polygon.real_verts()` to `polygon.true_verts()` to maintain naming consistency.
-   Rewrote `Rectangle` from the ground-up.
-   Window is now shown when begin is called. Not when init is called.
-   `mouse_button` key passed in mouse press events renamed to `button`

### Removed

-   `hitbox.get_obb()` because it wasn't working properly. Use `hitbox.get_aabb()` instead.
-   `polygon.transformed_verts()` because it was unused in the engine.
-   `camera.scale()`. Simply multiply by the zoom instead.
-   `Surf`, moving its functionality to `Surface` and updating `Raster` and `Image` accordingly.

### Fixed

-   Getting `Rectangle`, `Polygon`, or `Circle` components from a gameobject returning all `Hitbox` type objects.
    You can still replicate this functionality by passing `Hitbox` into the component getter.
-   Offsets (including rotational) not working properly. Physics has also been refactored to handle scaling properly.
-   `Rectangle` side getters and setters, which were not utilizing offsets properly. They now work with the AABB of the
    rectangle.
-   `gameobject.active` not functioning properly.

## [v3.1.0] - August 19, 2022

### Key Features

-   Made `Vector` a C class, improving overall Rubato performance.
-   Controller support!
-   `Surface` support! This is a class that lets you easily draw to a screen. The drawing is cached and is therefore
    very fast.
-   Increased performance by using `Surface` instead of `Draw` (3-4x improvement).

### Breaking Changes

-   As `Vector` is now a C class, it only holds floats and is therefore subject to floating point errors in unexpected cases.
    Be careful in accuracy-dependent calculations to handle deviation properly. Note that Python ints are implicitly cast to floats
    when used in Vector.
-   `Color.rgba32` is no longer a property is a method instead.
-   `Vector.one` and other similar class properties changed to classmethods, i.e. `Vector.one()`

### Added

-   `Group.all_gameobjects()` to get, recursively, all the game objects belonging to a group and its children.
-   Multiple `Event` types for controller events. Controllers are registered automatically by Rubato for event listening.
-   Assorted `Input` methods for querying the state of a controller.
-   `Raster` renamed to `Surface`.
-   `Raster` is now a component that holds a surface. It is analogous to `Image` for `Sprite`s.
-   Polygon filling algorithm for convex shapes
-   Line and circle/filling algorithms.

### Changed

-   Made `QTree` a C class. This is an internally used class and should not affect normal library usage.
-   Default drawing/debug colors from green to cyan.
-   Made rendering of images faster
-   `Polygon.generate_polygon` to `Vector.poly`. `generate_polygon` is deprecated and will be removed in a future update.

### Removed

-   `Game.name`, which did not do anything... yikes.
-   `Image.surface` is not accessible anymore. Instead use `Image.surf.surf`.
-   `flipx` and `flipy` are no longer available. Instead, set the scale to be negative.
-   `Vector.to_int()`. Use `Vector.floor()` or `Vector.round()` instead.

### Fixed

-   Deeply nested groups not colliding with ancestors
-   Hitboxes outside the boundaries not making use of QTrees properly

## [v3.0.0] - July 31, 2022

### Key Features

-   Optimized collision detection with Quadtrees, speeding up high-demand simulations significantly.

### Breaking Changes

-   z_indexes completely reworked.
-   Some setup, draw, and update methods deprecated in some classes.
-   Camera position is now where it looks at. ie. default camera position is now `Display.center`.
-   Reorder constructor parameters for most classes.
-   Removed `Game.scenes`, moving most `SceneManager` code into `Game`.
-   Renamed several internal `Time` attributes to better describe what they are.
-   Renamed `Vector.random_inside_unit_circle()` to `Vector.rand_unit_vector()`

### Added

-   `Component` now has a z_index
-   true_z property for components which gets the z_index of the `Component` offset by its parent `GameObject`
-   `Time.scheduled_call()` for a self-correcting recurring method call on a timed interval.
-   clone functions for `Group`, `GameObject`, and `Scene`.
-   `Draw.texture` and `Draw.queue_texture` to draw textures to the renderer
-   `Draw.sprite` and `Draw.queue_sprite` to draw sprites to the renderer
-   `Sprite` class to draw images that are not linked to Game Objects
-   `wrap()` function can create and populate a GameObject with component(s) automatically.
-   `world_mouse()` function to easily get the mouse position translated into world-coordinates
-   Support for operations with Vectors using tuples and lists, meaning less objects need to be created.
    (note that no length checking occurs, so make sure your tuples and lists are of length 2).
-   `raise_operator_error()` function to raise an error about an operator in a Pythonic style.
-   `Scene.switch()` instance method that allows users to switch to a scene without calling `Game.set_scene(scene_id)`
-   `Game.draw` and `Game.update` functions, both of which are overrideable, to give user-defineable functionality not reliant on scenes.
-   `Group.contains()` method for checking whether a group or gameobject has already been added to it.
-   `Hitbox.contains_pt` method for checking whether a point is inside a hitbox (useful in buttons and the like)

### Changed

-   Made `Time.now()` a function instead of a property.
-   Refactored collision detection code to not report contact points, since we don't need them anymore.
-   Added `hidden` attribute to all components and removed `visible` attribute from `Animation`, `Image`, and `Raster`
-   Moved `border_color` and `background_color` to individual `Scene` objects instead of a single attribute for the whole game.
-   Restructured the internal file heirarchy. Should not affect normal library useage at all.
-   Default border color in draw functions from `Color.green` to `Color.clear`
-   Use `Draw.{thing}` to draw immediately and `Draw.queue_{thing}` to draw with a specific z_index.
    (replace {thing} with the draw function of your choice)
-   Switching scenes now only takes effect on the next frame.
-   Reordered `Draw.clear` params to be more intuitive.
-   Renderer is automatically cleared if no scene exists.

### Removed

-   z_index from `Group`
-   Misc. unused draw, setup, and update methods for some classes.
-   Advanced rotational physics. Will be added in a later patch once Hitbox is refactored.
-   Vector `unit()` method. Use `normalized()` or `normalize()` instead.

### Fixed

-   Resizing an `Image` now works.
-   Updated all clone functions to work with new stuff.
-   Changing the camera zoom now affects all Sprites.
-   Made vector operations more complete and raise errors properly.
-   `Group.count()` not working properly.

## [v2.2.0] - June 12, 2022

### Breaking Changes

-   Removed all of the defaults dictionaries. Instead we are switching to a pythonic way of doing things. The key names, types, and defaults are still the same so its just a matter of adding \*\* to the beginning of the dictionary.
-   `Vector.angle` now returns the angle in degrees, starting from the top and going clockwise.
-   `Vector.from_radial` now matches the angle format described above and takes in an angle in degrees
-   `Vector.angle_between` now returns the angle in degrees.
-   `Color.random` now a function and not property. -> `Color.random()`
-   `Time.delta_time` and `Time.fixed_delta` are now in seconds instead of milliseconds
-   `Debug.*` all draw functions are moved to the Draw class. Default to Debug functionality.

### Added

-   `Display.get_window_border_size()` returns the size of the black bands around the window.
-   `Input.get_mouse_abs_pos()` returns the absolute position of the mouse.
-   `Display.border_size` fixed and integrated into `Input.get_mouse_pos()`: you only get on-renderer positions.
-   `Image.from_surface()` and `Image.from_buffer` functionality.
-   `Group.active` property. Boolean that controls whether the group is drawn and updated.
-   `Color.random_default()` Allows to randomly choose from a set of default colors.
-   `Debug` Added Debug module, that is called at the end of the game loop.
-   `Debug` Now shows docstring in documentation.

### Changed

-   `Math.sign()` now returns 0 for 0.
-   `time` module renamed to `rb_time` to not conflict with the Python time module.
-   `Draw` now has a default color of green.
-   `os.walk` Each function with os.walk has a recursive option now. To allow you to choose between recursive and shallow.
-   `window_pos` setting window_pos in init() now takes into account the border, so you set the topleft of the border.

### Fixed

-   `Vector.random_inside_unit_circle()` now actually returns a unit vector.
-   Fixed all Vector functions that had an angle in them to use north-degrees properly.
-   Added `Math.rad_to_north_deg()` and `Math.deg_to_north_rad()` to change accurately.
-   Fixed `error.deprecated()` to require a replacement or else it didn't work.

## [v2.1.1] - May 10, 2022

### Added

-   `Display` can now print the screen contents.
-   `Raster` for pixel mutation and drawing. (Separated from image)
-   `Display.border_size` returns the size of the black bands around the draw area.

### Changed

-   `Text.align` renamed to `Text.anchor` and is now properly documented.
-   `input` module renamed to `rb_input` to not override the built-in function.
-   `math` module renamed to `rb_math` to not override the built-in function.

### Removed

-   `Image` no longer has drawing functions. Instead use a `Raster` object.

### Fixed

-   `Text` font defaults was never actually being set if None. Now it is.
-   DLLs now actually bundle.

## [v2.1.0] - May 6, 2022

### Added

-   `Text` can now rotate.
-   `Button`. A button class that can be used to create a clickable area.
-   `end()`. Quits the game.
-   `pause()`. Pauses the game.
-   `resume()`. Resumes the game.
-   `penetration` and `normal` Manifold properties.
-   Removed and deprecated functionality is supported.
-   `colliding` set to Hitboxes that automatically updates with the hitboxes it is currently incident on.
-   `on_exit()` user defineable callback for hitboxes.
-   PyInstaller support.
-   All `Hitbox`s now have `get_aabb()` and `get_obb()` methods.
-   Can create a `RigidBody` with density instead of mass and moment. Will usually result in nicer behavior.
-   `Vector` now has a many quality of life methods. As well as rationalization.
-   `Math` fraction simplification, simplifying square roots, and prime number generation.

### Changed

-   Optimized draw cycle, effectively doubling framerates.
-   Some "to" and "from" methods for `Color`.
-   Significantly changed internal `Vector` functionality to allow custom pointers.
-   Moved the rotation parameters from `Component` to `Game Object`.
-   `Component` can now take in a dictionary of parameters.
-   Moved collision test code and impulse resolution to `Engine` class.
-   Changed default physics fps to 30.
-   `Polygon.generate_polygon()` can now takes an optional `options` parameter. When set, it returns a `Polygon` instead of a list of vertices.
-   Move basic draw functions from `Display` to `Draw`.

### Removed

-   `Vector`'s static method `is_vectorlike()`.
-   `Vector` instance method `translate()`. Use the `+` operator instead.
-   `Vector` instance method `transform()`. Use the `*` operator and `rotate()` instead.
-   Engine static method `overlap()`. Use the built in Hitbox `overlap()` method instead.
-   Removed `sep` property from Manifolds.
-   `Polygon`'s instance method `bounding_box_dimensions()`. This will be replaced by `get_bounds()` in a future patch.
-   `UIElement`. Instead use `Scene.add_ui()` with game objects.

## [v2.0.0] - April 5, 2022

### Added

-   Sound class rewritten
-   Spritesheet support
-   A full UI system
-   Text
-   Quick draw functions in `Display`

### Changed

-   Ported to PySDL2 from pygame
-   Moved all window management from `Game` to `Display`
-   Made classes that only need one instance static classes
-   Rectangle implementation is now distinct from polygons
-   Rename sprite to game object
-   `Input.key_pressed()` can now take in an arbitrary number of arguments

### Removed

-   Default sprite images

## [v1.2.0] - March 15, 2022

### Added

-   Proper 2d physics without angular velocity and torque
-   Circle collision
-   Groups are back

### Changed

-   Updated default image import to actually work properly
-   Hitboxes can now be colored in. This replaces the old Rectangle class
-   Hitboxes are now created like all other components (as in they use a options dictionary)
-   Collision now happen automatically

### Removed

-   Rectangle class

### Fixed

-   Animations are now independent from FPS

## [v1.1.0] - March 01, 2022

### Added

-   Sound system

### Changed

-   Switched to a component based system (similar to Unity)

### Removed

-   Removed Groups because they were deemed useless
-   Physics for now

## [v1.0.0] - Feb 01, 2022

### Added

-   Full Documentation through docstrings and through website
-   Loader for images. (Can load entire folders)
-   Custom errors
-   A full color implementation
-   Added continuous integration
-   Text can be drawn onto surfaces

### Changed

-   A more complete color implementation
-   New time system
-   Switched to GPL-3.0 License
-   Lots of linting
-   Move default options to their own area

### Fixed

-   Many many bugs

## [v0.0.1] - Nov 03, 2021

### Added

-   Basic framework for everything
-   Sprites, Scenes, Main game object
-   Rigidbody implementation

[unreleased]: https://github.com/rubatopy/rubato/
[v3.1.0]: https://github.com/rubatopy/rubato/tree/v3.1.0
[v3.0.0]: https://github.com/rubatopy/rubato/tree/v3.0.0
[v2.2.0]: https://github.com/rubatopy/rubato/tree/v2.2.0
[v2.1.1]: https://github.com/rubatopy/rubato/tree/v2.1.1
[v2.1.0]: https://github.com/rubatopy/rubato/tree/v2.1.0
[v2.0.0]: https://github.com/rubatopy/rubato/tree/v2.0.0
[v1.2.0]: https://github.com/rubatopy/rubato/tree/v1.2.0
[v1.1.0]: https://github.com/rubatopy/rubato/tree/v1.1.0
[v1.0.0]: https://github.com/rubatopy/rubato/tree/v1.0.0
[v0.0.1]: https://github.com/rubatopy/rubato/tree/v0.0.1
