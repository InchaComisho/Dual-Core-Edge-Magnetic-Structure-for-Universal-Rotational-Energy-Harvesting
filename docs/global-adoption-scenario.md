# Global Adoption Scenario Simulation
## Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting

---

## 1. Purpose

This document describes the **Global Adoption Scenario Simulator** for the Dual-Core Edge Magnetic Structure open generator architecture.

The simulator estimates how global distributed energy supply could change **if** this open generator concept were validated, manufactured at scale, and widely adopted across multiple sectors over the period 2026–2050.

This is a **scenario model** designed to explore a range of possible outcomes, not to predict what will happen. All numbers are derived from illustrative assumptions, not from measured hardware performance.

---

## 2. What Is Being Simulated

The simulator models five deployment sectors:

1. **Urban drainage and building water flow** — small units embedded in pipes, drains, and building water systems
2. **Agricultural irrigation and small canals** — units in irrigation channels and small water infrastructure
3. **Small river and micro-hydro sites** — units at micro-hydro locations with natural flow
4. **Distributed vertical-axis wind installations** — small vertical-axis wind turbines in urban, suburban, and rural settings
5. **Coastal tidal and wave-assisted rotational systems** — marine units capturing tidal and wave-driven rotation

For each sector and year from 2026 to 2050, the simulator estimates:

- cumulative installed units
- installed capacity (GW)
- annual electricity generation (TWh)
- avoided fossil electricity equivalent (TWh)
- avoided CO2 emissions (Mt CO2)
- share of global electricity demand (%)
- sensitivity to capacity factor and unit power assumptions

Five scenarios are modeled, ranging from conservative local pilots to a stress-test upper bound.

---

## 3. What Is NOT Being Claimed

This simulator does **not** claim:

- that the Dual-Core Edge Magnetic Structure has been physically built or validated
- guaranteed performance, efficiency, or output power
- free energy or perpetual motion
- that output energy can exceed input mechanical energy minus losses
- that these scenarios will occur or are likely
- that this technology will automatically replace existing energy systems
- that any specific deployment target is realistic without prototype validation
- that the assumed efficiency factors have been measured
- that conservation of energy is violated in any scenario

All parameters are illustrative. The simulator explicitly enforces conservation of energy: output is bounded by available mechanical input energy minus losses.

---

## 4. Sector Definitions

### Sector 1: Urban Drainage and Building Water Flow

Buildings and urban infrastructure generate continuous low-flow water movement in drainage systems, gray water circuits, HVAC cooling loops, and rooftop rainwater systems. A very small rotational generator embedded in these flows could harvest supplemental electricity. The default assumed unit power is 0.5 kW — extremely small. The main value is aggregate deployment at scale, not per-unit output.

### Sector 2: Agricultural Irrigation and Small Canals

Irrigation channels supply continuous water flow to agricultural land globally. A small generator at intake or distribution points could harvest energy from existing water movement without disrupting the irrigation function. Default assumed unit power is 2 kW. Maintenance in agricultural environments is assumed to be more challenging than urban settings.

### Sector 3: Small River and Micro-Hydro Sites

Micro-hydro is the most mature of the modeled sectors, with existing commercial examples. The Dual-Core Edge design could potentially lower manufacturing cost and simplify installation. Default unit power is 10 kW, capacity factor is 0.42 (reflecting seasonal flow variation). This sector has the highest per-unit energy density of the five.

### Sector 4: Distributed Vertical-Axis Wind

Vertical-axis wind turbines are appropriate for low-height, omnidirectional, and urban wind environments. Default capacity factor is 0.25, reflecting real-world VAWT performance in non-ideal conditions. Unit power is 5 kW. This sector is the most sensitive to local wind conditions and site selection.

### Sector 5: Coastal Tidal and Wave-Assisted

Marine environments provide persistent tidal and wave energy. The Dual-Core Edge design would require corrosion-resistant materials for saltwater deployment. Default unit power is 20 kW. Maintenance loss factor is highest here (0.12) due to marine exposure. This sector has the fewest deployment sites but the highest per-unit power.

---

## 5. Assumptions

All values below are illustrative defaults. They are labeled as assumptions, not measurements.

| Parameter | Urban Drainage | Irrigation | Micro-Hydro | Wind | Tidal |
|---|---|---|---|---|---|
| Unit power (kW) | 0.5 | 2.0 | 10.0 | 5.0 | 20.0 |
| Capacity factor | 0.30 | 0.35 | 0.42 | 0.25 | 0.38 |
| Efficiency factor | 0.55 | 0.58 | 0.62 | 0.55 | 0.60 |
| Maintenance loss | 0.08 | 0.10 | 0.08 | 0.10 | 0.12 |
| Grid integration loss | 0.05 | 0.08 | 0.06 | 0.07 | 0.08 |
| Fossil replacement fraction | 0.60 | 0.65 | 0.70 | 0.65 | 0.70 |
| Energy payback (years) | 3.0 | 3.5 | 4.0 | 4.0 | 5.0 |

Global reference parameters (placeholders — update with authoritative sources):

| Parameter | Default Value | Source Needed |
|---|---|---|
| Global electricity demand | 29,000 TWh/yr | IEA / BP Statistical Review |
| Global primary energy | 180,000 TWh/yr | IEA / BP Statistical Review |
| Fossil grid emission factor | 0.45 kg CO2/kWh | National/regional grid data |

Scenario scale multipliers:

| Scenario | Scale |
|---|---|
| conservative_local_adoption | 0.05 (5% of sites) |
| moderate_distributed_adoption | 0.20 (20% of sites) |
| accelerated_open_hardware_adoption | 0.50 (50% of sites) |
| infrastructure_integrated_adoption | 0.80 (80% of sites) |
| unrealistic_upper_bound_check | 1.00 (100% — stress test only) |

---

## 6. Formulas

### Installed Capacity

```
installed_capacity_gw = cumulative_units * average_unit_power_kw / 1,000,000
```

Units: kW → GW conversion by dividing by 10^6.

### Annual Generation

```
annual_generation_twh =
    installed_capacity_gw
    * capacity_factor
    * 8760
    / 1000
    * efficiency_factor
    * (1 - maintenance_loss_factor)
    * (1 - grid_integration_loss_factor)
```

- `8760` = hours per year
- Division by `1000` converts GW·h to TWh (since 1 TWh = 1000 GWh)
- `efficiency_factor ≤ 1.0` is required by conservation of energy
- `capacity_factor ≤ 1.0` means units are not always at rated power

### Avoided Fossil Electricity

```
avoided_fossil_twh = annual_generation_twh * replacement_fraction_of_fossil_energy
```

The replacement fraction represents the fraction of generated electricity that displaces fossil generation on the grid. This is not guaranteed to be 1.0 because renewable energy may displace other renewables or have limited grid access.

### Avoided CO2 Emissions

```
avoided_co2_mt =
    avoided_fossil_twh
    * 1,000,000,000     (TWh to kWh: 1 TWh = 10^9 kWh)
    * fossil_grid_emission_factor_kg_per_kwh
    / 1,000,000,000     (kg to Mt: 1 Mt = 10^9 kg)
```

Simplified: `avoided_co2_mt = avoided_fossil_twh * fossil_grid_emission_factor_kg_per_kwh`

### Deployment Growth

```
deployment_rate_year_n = deployment_rate_year_0 * (1 + annual_growth_rate)^n
```

Cumulative units are capped at `number_of_sites` to prevent unbounded growth.

### Sensitivity Analysis

- Capacity factor sensitivity: CF ± 0.05 applied to generation formula
- Unit power sensitivity: unit power × 0.7 (low) and × 1.3 (high)

---

## 7. Scenario Descriptions

### conservative_local_adoption

Slow, localized pilot deployments. Represents a world where the technology proves viable at small scale but faces regulatory, financial, or manufacturing barriers to wide adoption. 5% of estimated addressable sites reached by 2050.

**Interpretation:** Expected contribution is very small. This scenario shows the floor — what limited local deployment might achieve in isolation.

### moderate_distributed_adoption

Steady global uptake after prototype validation over 25 years. Represents reasonable policy support, open-hardware replication, and gradual integration into water and wind infrastructure. 20% of addressable sites reached by 2050.

**Interpretation:** A plausible trajectory if prototype validation succeeds and adoption scales with typical technology diffusion patterns.

### accelerated_open_hardware_adoption

Rapid replication after successful open-hardware publication. Assumes broad maker and NGO adoption, active replication in developing regions, and successful prototype validation. 50% of addressable sites reached by 2050.

**Interpretation:** Requires successful prototyping — not yet demonstrated. Should not be treated as a likely outcome at this stage.

### infrastructure_integrated_adoption

Deep embedding into water infrastructure planning globally. Requires policy mandates, engineering standards, and coordinated manufacturing. 80% of addressable sites reached by 2050.

**Interpretation:** Represents a world where distributed rotational energy harvesting becomes a standard layer of infrastructure design. Highly contingent on prototype validation, regulatory integration, and sustained investment.

### unrealistic_upper_bound_check (STRESS TEST ONLY)

**This is not a prediction. This is a stress test.**

100% of all estimated sites deployed at maximum rate. This scenario is physically and logistically implausible within the 2026–2050 window. It exists to:

- verify that the model handles upper bounds correctly
- confirm that conservation of energy guardrails remain active
- show what the theoretical ceiling would look like under impossible conditions

Any use of this scenario as a forecast or promotional claim is explicitly incorrect.

---

## 8. How to Run

### Requirements

- Python 3.8 or later (standard library only for core functionality)
- `matplotlib` optional (for PNG plot output)

### Run command

```bash
python simulation/global_adoption_scenario.py
```

### Outputs

| Output | Path |
|---|---|
| Console summary table | stdout |
| Full results CSV | `simulation/results/global_adoption_scenario.csv` |
| Generation by sector (if matplotlib) | `simulation/results/global_energy_contribution_by_sector.png` |
| Fossil replacement (if matplotlib) | `simulation/results/fossil_replacement_potential.png` |
| Adoption growth curve (if matplotlib) | `simulation/results/adoption_growth_curve.png` |

### Modifying parameters

Open `simulation/global_adoption_scenario.py` and modify:

- Global reference values near the top (clearly labeled as placeholders)
- `make_sector_*` functions to change sector defaults
- `build_scenarios()` to add, remove, or modify scenarios
- Scale multipliers in `build_scenarios()` to adjust scenario scope

---

## 9. How to Interpret Results

### Share of global electricity

The final column in the console table shows the percentage of global electricity demand that the modeled generation represents. Even in aggressive scenarios, this share remains small because:

- The units modeled are small distributed units (0.5–20 kW)
- Capacity factors are conservative
- Global electricity demand is large (~29,000 TWh/yr)

This is intentional. The value proposition of this architecture is **distributed supplemental energy**, not total replacement of grid-scale power.

### Sensitivity analysis

The CF sensitivity columns (lo/hi) show generation estimates if the capacity factor were 0.05 lower or higher. This reflects uncertainty in how often units actually run at rated power. The spread in these numbers indicates how sensitive results are to that assumption.

### Avoided CO2

Avoided CO2 numbers depend strongly on the assumed grid emission factor (0.45 kg/kWh by default). In regions with cleaner grids, avoided emissions are lower. Update this parameter with regional data for location-specific analysis.

### Stress test scenario

The unrealistic upper bound scenario will show numbers that look impressive but are flagged throughout as physically implausible. Do not cite these numbers as expected outcomes.

---

## 10. Limitations

1. **No physical prototype exists.** All efficiency factors, unit power values, and capacity factors are assumed. Actual performance may be higher or lower.

2. **Market and deployment assumptions are speculative.** The number of addressable sites, deployment rates, and growth rates are estimates with high uncertainty.

3. **Grid integration is not modeled in detail.** Real-world integration involves storage, grid stability, demand profiles, and curtailment that are not captured here.

4. **Sector independence is assumed.** The model does not account for interactions between sectors or resource competition.

5. **No manufacturing, material, or cost analysis.** The simulator does not model supply chains, raw material constraints, or economic viability.

6. **No ecosystem or ecological impact modeling.** Some sectors (tidal, irrigation) could affect local ecosystems. This is not modeled.

7. **Climate feedback is not modeled.** The simulator does not model how avoided CO2 affects climate trajectories.

8. **Fixed global electricity demand.** In reality, demand grows over time. Using a fixed baseline overestimates the percentage share in later years.

---

## 11. Why Distributed Rotational Energy Harvesting Could Matter

Most current renewable energy development focuses on centralized, large-scale installations: utility-scale solar farms, offshore wind, large hydroelectric dams. These are effective and necessary, but they leave a large category of energy largely untapped: **small, distributed, persistent mechanical flows**.

Urban drainage, irrigation channels, small rivers, coastal tides, and building water systems collectively represent a vast number of low-power, continuously available energy flows. They are often close to points of consumption. They do not require large transmission infrastructure. They operate at scales compatible with local microgrids and off-grid applications.

If a modular, low-maintenance, low-cost rotational generator architecture can be validated, the aggregate contribution of many small units could become meaningful as a **distributed supplemental energy layer** — not replacing centralized power, but adding resilience and local generation capacity.

The Dual-Core Edge Magnetic Structure is a concept that could potentially lower the cost and complexity of such a generator module. Whether it succeeds depends entirely on physical prototyping and measurement.

---

## 12. What Measurements Are Needed Before Real-World Claims

Before any result from this simulator can be cited as a real-world projection, the following must be demonstrated through physical testing:

| Required Measurement | Why Needed |
|---|---|
| RPM vs. open-circuit voltage curve | Validates electromagnetic model |
| Torque vs. load curve | Allows calculation of mechanical input power |
| Efficiency at rated and partial load | Replaces assumed efficiency_factor with measured value |
| Thermal performance under sustained operation | Confirms that assumed losses are realistic |
| Durability in water, wind, and marine environments | Validates maintenance_loss_factor assumptions |
| Startup torque and minimum flow threshold | Determines real-world capacity factor |
| Comparison against existing generators of similar size | Provides context for the dual-core design's contribution |
| Long-term corrosion and fouling behavior (marine sectors) | Validates deployment lifetime assumptions |

Until these measurements exist, **all numbers in this simulator are illustrative**.

---

## 13. Policy and Infrastructure Implications

If prototype validation succeeds, the following policy areas become relevant:

- **Building codes**: Mandate or incentivize generator integration in new drainage and HVAC systems
- **Agricultural subsidies**: Support irrigation-integrated energy harvesting as a dual-use infrastructure investment
- **Open hardware standards**: Establish measurement and safety standards for distributed micro-generators
- **Grid interconnection rules**: Simplify interconnection requirements for very small distributed generators (< 10 kW)
- **Marine permitting**: Create streamlined permit pathways for small tidal units that do not require large environmental assessments
- **Development finance**: Fund open-hardware replication in low-income regions where centralized grid infrastructure is limited

None of these implications assume the technology works. They are contingent on successful prototyping.

---

## 14. Open Invention Significance

This simulator was built to accompany an **open invention disclosure**, not a commercial product announcement.

The Dual-Core Edge Magnetic Structure is published under Creative Commons CC BY 4.0. Anyone may prototype, test, modify, or commercialize it. The open publication is intended to:

- prevent the concept from being buried in a closed patent portfolio
- enable global independent replication at low cost
- ensure that if the concept works, its benefits can spread without licensing barriers
- invite critique, which is the only way to improve the design

Open hardware energy inventions have historically had slower adoption than proprietary technologies, partly because no single actor has financial incentive to invest in their validation. This simulator is one tool for making the potential value of such validation visible — without overstating what is known.

The honest position is: **this is a concept that deserves a prototype, not a guaranteed solution**.

---

*Document version: 2026-06-06*  
*Repository: InchaComisho/Dual-Core-Edge-Magnetic-Structure-for-Universal-Rotational-Energy-Harvesting*  
*License: CC BY 4.0*
