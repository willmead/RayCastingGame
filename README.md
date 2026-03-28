# Raycasting Game

## Introduction

This is a project to explore implementing a raycasting engine to make a game similar in aesthetic to the old wolfenstein-style games. 

## TODO

- [x] Implement untextured raycasting to draw walls
- [x] Implement textured raycasting to draw walls
- [x] Implement textured raycasting to draw floor and ceiling
- [ ] Add simple sprites (always face player)
- [ ] Add sprite animations
- [ ] Use ECS to keep track of entities


## Notes

* Implementation of textured floors is not only messy, it is slow, I have tried optimizing it but I think there is more to be done, either lower the resolution of the game and scale up or use a different algorithm to simplify the process.