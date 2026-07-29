# Not Prosthetics

- URL: https://www.lesswrong.com/posts/2XCN7rAdMMMeDJGkG/not-prosthetics
- Author: Elliot Callender
- Date: 2026-05-27
- Karma: 11  Comments: 0  Words: 467
- Band: C  Tier: 2  Score: 30.9  Density: 8.57
- Anchors: \bcursor\b

---

BCI firms have received heavy investment in the past few years. This is great, and I'm proud that humanity is restoring agency to recipients! But existing market pressures aren't going to make superhumans.

Every interesting BCI intelligence enhancement approach I can think of needs extremely high resolution:

*   [Accelerating sleep-based skill acquisition](https://www.lesswrong.com/posts/uzL9xLj6pwaij5TyK/accelerated-skill-learning-via-dream-engineering-and)[^y1alx48fvt]
*   [Increasing effective brain mass / "general compute"](https://www.lesswrong.com/posts/ewZXQgzaCvzdSvtWE/biologically-plausible-sgd-is-hard)
*   [Expanding working memory](https://www.lesswrong.com/posts/DAFMA6aqDyGNXAaJe/working-memory-expansion)
*   [Neuralese/telepathy](https://www.lesswrong.com/s/Wy8smXGZ7PsS9CpgP/p/6ouGcnFSyBjJzEA5b)

Yet every existing major neurotech lab has physiologically and behaviorally narrow targets with minimal bandwidth:

*   **Neuralink** runs ~1k thread electrodes in motor cortex which decode into a small set of actions (cursor movement, eventually speech decoding / limb control)
*   **Synchron**'s stentrode places ~16 channels endovascularly for motor intent in ALS patients; again minimally invasive, sensible for FDA approval
*   **Paradromics**' CONNEXUS is ~1.6k channels targeting speech, although they have very interesting tech
*   **Precision Neuroscience** uses a surface array at ~4k channels for prosthetics
*   **Blackrock Neurotech**'s Utah arrays have 128 channels and are too rigid for long-term insertion
*   **Science Corporation** uses similar tech to what I'm proposing but is currently constrained to ~1k channels
*   **Merge Labs**' *stated goals* are closest to mine. Merge, if I'm [reading](https://www.merge.io/blog) them right, aims for an interconnect density in the hundreds of millions to billions. Their technology sounds to me *at least* a decade away with massive AI uplift (or 30 years without uplift)[^grvwtwh5e4n]
*   **Neuropixels Ultra** is a research probe meant for non-human animals; it destructively slices tissue to read depth-based signaling. NP Ultra can pull 384 channels out of ~6.1k total, which is less total bandwidth but [~20x the density](https://www.cell.com/neuron/fulltext/S0896-6273\(25\)00665-8) of prosthetic contenders. They don't send signals back to the brain and are thermally limited to pulling from a small subset of their electrodes

So mostly motor and speech regions, with a few thousand connections. That's sufficient for decoding cursor velocity, intended phoneme, visual stimulus class, etc engineered features. These are tasks where a small, well-chosen set of channels in a known-functional region carries enough information that work on the decoder side does the rest. Pushing higher is worse for biocompatibility, R&D cost, and regulatory clearance.

Again, to be clear, I think these labs are doing interesting and important work.

But if you want to talk to the brain like it talks to itself (see [Bitter Lesson](https://en.wikipedia.org/wiki/Bitter_lesson)), you need a few hundred million connections. This immediately causes transmission and thermal issues. Whereas Neuralink uses low-power Bluetooth, we need multiple bidirectional fiber optics, an external power supply, and probably an active cooler cycling fluid between the skull and a radiator.

I would be very surprised if the FDA and insurers approved "permanent bundle of cables and pipes exiting patient's head", particularly since "wants to solve AI alignment" is not yet a medical indication[^w1fqquz288].

[^y1alx48fvt]: Dream engineering was the most interesting thing I read about in grade school. 

[^grvwtwh5e4n]: Reading individual neurons through skull (or even dura), or inferring similarly useful signals without access to individual neurons, seems extremely difficult. Merge claims that they can do something close to this molecularly and/or with ultrasound; but molecules diffuse slowly and in all directions, so I'm unsure how they plan to achieve spatial and temporal precision. Ultrasound may eventually work, but it's unclear to me how to avoid the signal distortion of crossing multiple material boundaries, whether that's a soundwave or something more exotic. Perhaps magnetic sensors? I'm all for speculative BCI tech; I just think that non-invasive approaches won't happen before ASI. 

[^w1fqquz288]: Maybe one could market for intellectually disabled folks. I still think cable management is a hard no for most would-be patients.