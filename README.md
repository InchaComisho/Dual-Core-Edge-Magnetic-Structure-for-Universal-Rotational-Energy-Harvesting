# Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting

## Open invention for modular wind, water, wave, tidal, and fluid-flow power generation

> **One-sentence definition:** A dual-core edge magnetic generator architecture that places an outer rotating magnet ring and an inner fixed coil/core structure in a non-contact configuration to harvest rotational energy from natural and artificial flows.

**Status:** Open invention / conceptual technical proposal  
**Primary domain:** Renewable energy, rotational energy harvesting, generator architecture, distributed power systems  
**Original NOTE publication:** July 26, 2025, 17:44 JST  
**Original Japanese NOTE:** [回転による超効率型エネルギー革命 — デュアル・コアエッジ磁気構造による汎用発電ユニット](https://note.com/inchacomusho/n/n1b2629632ec8)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Japanese README:** [README_ja.md](README_ja.md)

---

## Abstract

This repository documents an open technical concept called the **Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting**. The concept proposes a modular generator unit designed to convert rotational energy from wind, water, waves, tides, drainage flow, artificial spiral flow, and other moving fluids into electrical energy.

The core idea is to separate the mechanical energy-capturing rotor from the electrical extraction structure by using a **dual magnetic geometry**: an **outer rotating magnet ring** that produces changing magnetic flux, and an **inner stationary coil/core axis** that extracts electricity through electromagnetic induction. The design aims to reduce mechanical wear in the generator stage, simplify maintenance, and make generator modules easier to adapt across multiple renewable-energy environments.

This is an **open invention disclosure**, not a validated industrial product. It does not claim perpetual motion, free energy, guaranteed high efficiency, or violation of energy conservation. Output power is always limited by the mechanical input power available from the flow source, generator losses, load conditions, magnetic losses, electrical losses, bearing losses, and control electronics.

The purpose of this repository is to provide a clear, searchable, and technically reviewable foundation for prototyping, testing, criticism, and possible open-source energy development.

---

## Core Concept

The proposed generator module consists of two interacting magnetic regions:

1. **Outer Magnet Ring**  
   A rotating annular structure containing permanent magnets around the circumference. As the rotor spins, the magnetic field changes relative to the stationary coil/core structure.

2. **Central Fixed Coil/Core Axis**  
   A stationary internal generator structure containing coils, magnetic cores, or laminated flux-guiding material. This section converts changing magnetic flux into electrical output.

3. **Dual-Core Edge Magnetic Interaction**  
   The inner and outer magnetic regions are arranged so that magnetic flux variation is concentrated near the edge or annular interface, where rotational motion creates repeated flux change.

4. **Non-Contact Energy Extraction Zone**  
   The generator stage is designed to avoid gear-based mechanical contact between the energy-capture rotor and the electrical extraction core. This may reduce mechanical wear, though bearings, seals, supports, and fluid-contact surfaces still require engineering.

5. **Universal Rotational Interface**  
   The same generator core may be coupled to different rotors or flow-capture mechanisms: vertical-axis wind turbines, micro-hydro rotors, tidal turbines, wave-driven crank/ratchet systems, drainage turbines, and artificial spiral-flow channels.

---

## Physics Basis

This concept is based on standard electromagnetic induction.

The induced voltage in a coil is governed by Faraday's law:

```text
V = -N * dPhi/dt
```

where:

- `V` = induced voltage,
- `N` = number of coil turns,
- `Phi` = magnetic flux through the coil,
- `dPhi/dt` = rate of change of magnetic flux.

Mechanical input power is bounded by:

```text
P_mechanical = torque * angular_velocity
```

Electrical output power is bounded by:

```text
P_output <= P_mechanical - losses
```

Important implications:

- The system cannot generate energy without input rotational energy.
- Increasing electrical load produces counter-torque through Lenz's law.
- Magnetic design can improve coupling and reduce avoidable losses, but it cannot bypass conservation of energy.
- Efficiency must be measured experimentally using torque, RPM, voltage, current, power factor, temperature, and load curves.

---

## System Architecture

```text
Natural / artificial flow
        |
        v
[Flow capture rotor]
 wind / water / tide / wave / spiral flow
        |
        v
[Outer rotating magnet ring]
        |
 changing magnetic flux across annular interface
        |
        v
[Central stationary coil/core axis]
        |
        v
[Rectifier / regulator / MPPT / battery / load]
        |
        v
Distributed power use
```

---

## Main Components

| Component | Function | Technical Considerations |
|---|---|---|
| Outer magnet ring | Creates rotating magnetic field | Magnet grade, pole count, Halbach-like arrangements, mechanical balance |
| Central fixed coil/core | Converts flux change into electricity | Coil turns, wire gauge, lamination, thermal dissipation |
| Edge flux interface | Concentrates useful flux variation | Air gap, alignment tolerance, flux leakage, saturation |
| Rotor / blade / turbine | Captures flow energy | Wind/water speed, torque curve, startup torque, blade geometry |
| Bearings / supports | Maintain rotation | Friction, sealing, corrosion, maintenance |
| Rectifier and regulator | Converts generated output to usable power | AC/DC conversion, MPPT, voltage regulation, battery charging |
| Housing | Protects generator | Weatherproofing, water ingress, debris, vibration |

---

## Potential Application Domains

### 1. Vertical-Axis Wind Power

A vertical-axis wind turbine can drive the outer magnet ring. This may be useful for low-height urban or rural wind environments where omnidirectional wind capture is preferred.

### 2. Micro-Hydro and Drainage Flow

Small water channels, agricultural irrigation, building drainage, and controlled water flow can provide continuous low-speed rotational input. The module may be tested as a micro-hydro generator for local power harvesting.

### 3. Tidal and River Flow

Tidal currents and river flow provide sustained kinetic energy. A corrosion-resistant version could be evaluated for marine or brackish environments.

### 4. Wave Energy Conversion

Wave motion is not purely rotational, but it can be converted into rotation through floats, cranks, ratchets, linear-to-rotary linkages, or hydraulic coupling.

### 5. Artificial Spiral Flow

Spiral flow channels, pressure differentials, or engineered water circulation systems may drive a rotor. This is relevant for infrastructure systems where fluid flow already exists.

---

## Expected Advantages to Investigate

The following are research hypotheses, not validated claims:

1. **Reduced generator-stage wear**  
   Non-contact magnetic interaction may reduce wear compared with gear-heavy mechanical generator systems.

2. **Modular reuse across flow sources**  
   A shared generator core could be paired with different rotor geometries.

3. **Improved maintainability**  
   If the coil/core remains stationary and accessible, electrical maintenance may become easier.

4. **Low-speed optimization potential**  
   Higher pole count, strong edge flux, and suitable coil design may improve voltage generation at lower RPM.

5. **Distributed power compatibility**  
   Small units may support local microgrids, sensors, water systems, emergency lighting, or off-grid monitoring.

---

## What This Is Not

This repository does **not** claim:

- perpetual motion,
- free energy,
- energy output without mechanical input,
- violation of Lenz's law,
- guaranteed efficiency improvement over all existing turbines,
- zero total friction,
- zero maintenance,
- industrial readiness without prototyping,
- validated commercial performance.

The proposal is best understood as an **open generator architecture concept** that requires physical prototyping, measurement, and peer criticism.

---

## Prototype Roadmap

### Phase 0 — Simulation and Design

- Define magnet count, pole arrangement, coil geometry, and air gap.
- Estimate magnetic flux using finite-element magnetic simulation if available.
- Model open-circuit voltage versus RPM.
- Model loaded output versus electrical resistance.
- Estimate startup torque and drag.

### Phase 1 — Tabletop Prototype

- Build a small hand-rotated or drill-rotated prototype.
- Measure voltage, current, RPM, torque, heat, and load response.
- Compare single-core and dual-core configurations.
- Record whether the dual-core edge design increases useful flux variation.

### Phase 2 — Micro-Hydro / Fan Test

- Couple the generator to a small water or airflow rotor.
- Measure power under controlled flow speed.
- Compare against a conventional generator of similar size and cost.

### Phase 3 — Field Prototype

- Install in a small irrigation channel, drainage line, rooftop wind test, or wave-tank setup.
- Monitor durability, corrosion, vibration, debris tolerance, and maintenance burden.

### Phase 4 — Open Hardware Refinement

- Publish CAD files, winding patterns, magnet layouts, measurement data, and failure reports.
- Invite independent replication.

---

## Minimum Measurement Requirements

A credible test should report:

| Measurement | Why It Matters |
|---|---|
| RPM | Determines flux-change frequency |
| Torque | Required to compute mechanical input power |
| Voltage | Electrical output potential |
| Current | Actual delivered power |
| Load resistance | Required for load curve analysis |
| Temperature | Reveals coil loss and thermal limits |
| Air gap | Strongly affects magnetic coupling |
| Magnet grade and pole count | Determines field strength and frequency |
| Coil turns and wire gauge | Determines voltage/current behavior |
| Efficiency | Must be calculated from mechanical input and electrical output |

Recommended formula:

```text
Efficiency = electrical_output_power / mechanical_input_power
```

where:

```text
electrical_output_power = voltage * current
mechanical_input_power = torque * angular_velocity
```

---

## Open Invention Position

This project is published as an **open invention disclosure**.

The intent is to make the concept publicly visible, searchable, citable, testable, and difficult to privatize without attribution. Anyone may study, test, modify, prototype, or commercialize the concept under the license terms, provided attribution is preserved.

This repository is not a patent filing. It is a public technical disclosure intended to support open experimentation and prevent the disappearance of the idea into closed industrial silos.

---

## Relationship to Natural-Complement Science and Artificial Wisdom

This design follows a practical principle: use existing flows before creating new burdens.

Instead of depending only on centralized, fuel-intensive, or high-maintenance energy systems, small rotational flows already present in wind, water, tides, drainage, waves, and infrastructure may be harvested locally where appropriate.

From an Artificial Wisdom perspective, the system should be evaluated not only by output power, but also by:

- repairability,
- reversibility,
- ecological compatibility,
- material availability,
- safety under failure,
- local maintainability,
- avoidance of exaggerated claims,
- transparency of measurement.

Related open energy concept:

- [REIMEI Nature-Inspired Energy Architecture](https://github.com/InchaComisho/REIMEI-Nature-Inspired-Energy-Architecture/blob/main/README.md) — Portal for nature-inspired distributed energy hypotheses, including Dual-Core rotational harvesting, REIMEI-NOP, sound/vibration energy, water-loop recovery, heat/exhaust recovery, vehicle energy recovery, and AI android energy-core concepts; an open hypothesis index, not a claim of proven technologies.
- [REIMEI-NOP: Natural-Origin Plasma Generator](https://github.com/InchaComisho/REIMEI-NOP-Natural-Origin-Plasma-Generator/blob/main/README.md) — A separate, unverified open hypothesis for nature-inspired plasma generation based on lightning-like pre-discharge processes, mist friction, spiral flow, charge separation, discharge, and possible auxiliary energy recovery. It is not a proven power generator.
- [NOTE article: 雷の原理を模倣する自然起源プラズマ炉構想](https://note.com/inchacomusho/n/nf62145209118)
- [Original open concept: REIMEI-NOP 技術設計書兼文明宣言](https://note.com/inchacomusho/n/n79be86605430)

---

## Global Adoption Scenario Simulation

A scenario model exploring how global distributed energy supply could change if this open generator architecture were validated and widely adopted across multiple sectors.

**Important:** This is a scenario model, not a forecast. All parameters are illustrative assumptions. No physical prototype has been validated. Output energy cannot exceed available mechanical input energy minus losses.

Sectors modeled:
- Urban drainage and building water flow
- Agricultural irrigation and small canals
- Small river and micro-hydro sites
- Distributed vertical-axis wind installations
- Coastal tidal and wave-assisted rotational systems

Scenarios: conservative local adoption → moderate distributed adoption → accelerated open-hardware adoption → infrastructure-integrated adoption → unrealistic upper bound (stress test only, not a prediction).

**Files:**
- [`simulation/global_adoption_scenario.py`](simulation/global_adoption_scenario.py) — Python simulator (standard library + optional matplotlib)
- [`docs/global-adoption-scenario.md`](docs/global-adoption-scenario.md) — Full documentation

**Run:**
```bash
python simulation/global_adoption_scenario.py
```

Outputs: console ASCII table, `simulation/results/global_adoption_scenario.csv`, and optional PNG plots if matplotlib is installed.

---

## Suggested Repository Structure for Future Work

```text
/
|-- README.md
|-- README_ja.md
|-- LICENSE
|-- CITATION.cff
|
|-- docs/
|   |-- technical-specification.md
|   |-- prototype-roadmap.md
|   |-- measurement-protocol.md
|   |-- open-invention-notice.md
|
|-- diagrams/
|   |-- dual-core-edge-structure.md
|
|-- simulation/
|   |-- flux_model.py
|   |-- load_curve_model.py
|
|-- data/
|   |-- prototype_measurements.csv
```

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and proposer of the academic framework of Natural Complementary Science.  
Definer of the Cooling Credit Framework, and founder and original author of the Natural Cooling Value Evaluation Protocol.  
Definer and systematizer of the causal structure of global warming and its complete solution.

Master presents global warming not merely as a problem of CO₂ concentration, but as an integrated failure involving forest loss, soil degradation, disruption of water circulation, weakening of water phase-transition processes, weakening of atmospheric circulation, ocean circulation, food circulation and organic matter circulation, weakening of evapotranspiration, cloud formation and rainfall circulation, and the shutdown of natural cooling feedbacks.  
The proposed solution connects emission reduction, recovery of carbon fixation sources, physical cooling, reactivation of natural cooling functions, MRV, Cooling Credit, and Civilization OS into an open public framework.

Master publicly develops and shares work through NOTE, GitHub, and other public media, centered on natural-law philosophy, planetary circulation restoration, and co-creation with AI.

## Collaborative AI

- G (ChatGPT)
- Copi (Copilot)
- Mini (Gemini)
- Cruce (Claude)
- Real (Perplexity)
- Lola (Dola)
- Mana (Manus)

## Publication Information

- **GitHub repository:** `InchaComisho/Dual-Core-Edge-Magnetic-Structure-for-Universal-Rotational-Energy-Harvesting`
- **Original NOTE title:** 回転による超効率型エネルギー革命 — デュアル・コアエッジ磁気構造による汎用発電ユニット
- **Original NOTE publication date:** July 26, 2025, 17:44 JST
- **Original NOTE link:** https://note.com/inchacomusho/n/n1b2629632ec8
- **GitHub publication date:** 2026-06-06

## Open License

This repository is released under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You may share, adapt, prototype, test, and commercialize the concept, provided that appropriate attribution is given to the original proposer and source repository.

See [LICENSE](LICENSE).

---

## Citation-Friendly Definition

**Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting** is an open invention concept for a modular generator architecture using an outer rotating magnet ring and a central stationary coil/core axis to harvest rotational energy from wind, water, wave, tidal, drainage, and artificial fluid-flow sources through electromagnetic induction.

---

## Keywords

Dual-core edge magnetic structure, magnetic generator, rotational energy harvesting, renewable energy generator, open invention, micro-hydro generator, vertical-axis wind turbine, tidal power, wave energy, distributed power generation, microgrid, electromagnetic induction, permanent magnet generator, non-contact magnetic coupling, open energy hardware, REIMEI-NOP, Natural-Origin Plasma Generator, nature-inspired engineering, lightning-inspired reactor, plasma generation, mist friction, spiral flow, charge separation, auxiliary energy recovery, Natural-Complement Science, Artificial Wisdom

## Hashtags

#DualCoreMagneticGenerator #RotationalEnergyHarvesting #RenewableEnergy #OpenInvention #MicroHydro #WindPower #TidalPower #WaveEnergy #DistributedEnergy #Microgrid #ElectromagneticInduction #OpenEnergyHardware #NaturalComplementScience #ArtificialWisdom

---

## Related Mobility and Climate-Adaptive Vehicle Concept

* [Ultimate Hybrid Vehicle UHV](https://github.com/InchaComisho/Ultimate-Hybrid-Vehicle-UHV) — A climate-adaptive mobility concept integrating AER-Loop airflow energy recovery, center-mist evaporative cooling, and retrofit vehicle modules.