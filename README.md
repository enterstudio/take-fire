# take-fire
Batch transfer selected FIRE simulation snapshots and halo files

## About

Usually I don't need all the snapshots from a simulation for my analysis, so I only transfer those needed to save traffic and space. This project makes it easy to specify such a transfer in a json file and to carry it out through Globus. Prior knowledge about [FIRE](http://fire.northwestern.edu/) and [Globus](https://www.globus.org/) is assumed.

## Example

```bash
python download.py example-task.json
```
