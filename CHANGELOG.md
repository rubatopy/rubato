# Changelog

## [Unreleased]

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

### Changed

-   Optimized draw cycle, effectively doubling framerates.
-   Some "to" and "from" methods for `Color`.
-   Significantly changed internal `Vector` functionality to allow custom pointers.
-   Moved the rotation parameters from `Component` to `Game Object`.
-   `Component` can now take in a dictionary of parameters.
-   Moved collision test code and impulse resolution to `Engine` class.
-   Changed default physics fps to 30.
-   `Polygon.generate_polygon()` can now takes an optional `options` parameter. When set, it returns a `Polygon` instead of a list of vertices.

### Removed

-   `Vector`'s static method `is_vectorlike()`.
-   `Vector` instance method `translate()`. Use the `+` operator instead.
-   `Vector` instance method `transform()`. Use the `*` operator and `rotate()` instead.
-   Engine static method `overlap()`. Use the built in Hitbox `overlap()` method instead.
-   Removed `sep` property from Manifolds.
-   `Polygon`'s instance method `bounding_box_dimensions()`. This will be replaced by `get_bounds()` in a future patch.
-   `UIElement`. Instead use `Scene.add_ui()` with game objects.

### Fixed

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

[unreleased]: https://github.com/rubatopy/rubato/tree/main
[v2.0.0]: https://github.com/rubatopy/rubato/tree/v2.0.0
[v1.2.0]: https://github.com/rubatopy/rubato/tree/v1.2.0
[v1.1.0]: https://github.com/rubatopy/rubato/tree/v1.1.0
[v1.0.0]: https://github.com/rubatopy/rubato/tree/v1.0.0
[v0.0.1]: https://github.com/rubatopy/rubato/tree/v0.0.1
