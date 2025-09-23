
# Change Log
All notable changes to this project will be documented in this file.

## [0.2.1] - 2025-09-24
### Added
- Model selection based on display context
  - Display using the `PlayingCards_lg` variant within item frames
  - Display as blank in thirdperson view (No more peeking!)

## [0.2.0] - 2025-09-22
### Added
- Support for 1.21.4+ item model format
- Use of `equippable` component to support wearing paper in the head slot
- New card model layers to individually texture suit, value, and overlay

### Changed
- Restructured models and textures based on suit and value

### Removed
- Old card models and textures


## [0.1.3] - 2024-10-01
### Added
- Red and black joker textures

### Changed
- Item models now render faced down on the ground


## [0.1.2] - 2024-09-01

### Added
- Variants! To be used in addition to the base pack
  - `PlayingCards_lg` adjusted to be displayed larger in item frames
  - `PlayingCards_canton` with alternate textures
- Models for jokers (untextured) and card with 2 backs
- Custom card names with localization support

### Changed
- Centered models around pivot point


## [0.1.1] - 2024-08-26
Minor changes to data pack
 
### Added
- Recipe to obtain a deck of (paper) cards via crafting
- Function `cards:deck_wearable` for the carved pumpkin deck 
- Deck function

### Changed
- Renamed directories to be version agnostic
- Function `cards:deck` now gives remodeled paper instead of pumpkins

### Fixed
- Inconsistent texture for the Ace of Diamonds
 
## [0.1.0] - 2024-08-24
Initial release
 
### Added
- Card models and textures
- Function `cards:deck` to obtain a deck of cards