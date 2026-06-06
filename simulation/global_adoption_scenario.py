"""
Global Adoption Scenario Simulator
Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting

IMPORTANT DISCLAIMERS:
  - This is a scenario model, NOT a forecast or prediction.
  - All parameters are illustrative assumptions, NOT measured hardware performance.
  - No physical prototype of this generator architecture has been built or validated.
  - Output energy cannot exceed available mechanical input energy minus losses.
  - This script explicitly obeys conservation of energy.
  - Numbers in this simulator do NOT imply guaranteed performance.
  - This is not a claim of free energy or perpetual motion.
  - Results require physical prototype validation before any real-world claims.
  - Update global reference parameters with authoritative data before use.

Formula reference:
  annual_generation_twh =
      installed_capacity_gw
      * capacity_factor
      * 8760          (hours per year)
      / 1000          (GW -> TW unit conversion)
      * efficiency_factor
      * (1 - maintenance_loss_factor)
      * (1 - grid_integration_loss_factor)

  avoided_fossil_twh = annual_generation_twh * replacement_fraction_of_fossil_energy

  avoided_co2_mt =
      avoided_fossil_twh
      * 1e9            (TWh -> kWh)
      * fossil_grid_emission_factor_kg_per_kwh
      / 1e9            (kg -> Mt)

Usage:
  python simulation/global_adoption_scenario.py

Outputs:
  - Console ASCII summary table
  - simulation/results/global_adoption_scenario.csv
  - simulation/results/global_energy_contribution_by_sector.png  (if matplotlib)
  - simulation/results/fossil_replacement_potential.png          (if matplotlib)
  - simulation/results/adoption_growth_curve.png                 (if matplotlib)
"""

import os
import csv
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# ---------------------------------------------------------------------------
# GLOBAL REFERENCE PARAMETERS
# PLACEHOLDER VALUES -- update with authoritative data before use.
# Sources: IEA, Our World in Data, BP Statistical Review, etc.
# ---------------------------------------------------------------------------

GLOBAL_ELECTRICITY_DEMAND_TWH = 29_000.0   # placeholder: ~2023 global electricity (TWh)
GLOBAL_PRIMARY_ENERGY_TWH = 180_000.0       # placeholder: ~2023 global primary energy (TWh)
FOSSIL_GRID_EMISSION_FACTOR_KG_PER_KWH = 0.45  # placeholder: average grid emission factor
START_YEAR = 2026
END_YEAR = 2050

# Physical plausibility guardrails
MAX_PLAUSIBLE_CAPACITY_FACTOR = 0.60        # no flow source sustains above ~60% CF long-term
MAX_PLAUSIBLE_EFFICIENCY = 0.92             # no generator exceeds ~92% under real conditions
MAX_PLAUSIBLE_UNIT_POWER_KW = 500.0         # single small distributed unit upper bound (kW)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


# ---------------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------------

@dataclass
class SectorConfig:
    """Configuration for one deployment sector."""
    name: str
    description: str
    number_of_sites: int              # total eventual addressable sites (scenario-specific)
    average_unit_power_kw: float      # kW per installed unit (illustrative)
    capacity_factor: float            # fraction of time at rated power (0..1)
    deployment_rate_per_year: int     # new units deployed per year
    annual_growth_rate: float         # fractional growth in deployment rate per year
    efficiency_factor: float          # generator efficiency (0..1)
    maintenance_loss_factor: float    # fractional loss due to downtime/maintenance
    grid_integration_loss_factor: float  # fractional loss in transmission/integration
    replacement_fraction_of_fossil_energy: float  # fraction of output displacing fossil
    manufacturing_energy_payback_years: float  # years to pay back embodied energy


@dataclass
class ScenarioConfig:
    """Top-level scenario definition."""
    name: str
    description: str
    is_stress_test: bool
    sectors: List[SectorConfig]


@dataclass
class YearResult:
    """Computed results for a single year, single sector."""
    year: int
    sector_name: str
    cumulative_units: int
    installed_capacity_gw: float
    annual_generation_twh: float
    avoided_fossil_twh: float
    avoided_co2_mt: float
    share_of_global_electricity_pct: float
    capacity_factor_sensitivity_low_twh: float   # CF - 0.05
    capacity_factor_sensitivity_high_twh: float  # CF + 0.05
    unit_power_sensitivity_low_twh: float        # unit_power * 0.7
    unit_power_sensitivity_high_twh: float       # unit_power * 1.3
    warnings: List[str]


# ---------------------------------------------------------------------------
# SECTOR PRESETS
# These are ILLUSTRATIVE defaults. All values are assumed, not measured.
# ---------------------------------------------------------------------------

def make_sector_urban_drainage(scale: float = 1.0) -> SectorConfig:
    return SectorConfig(
        name="urban_drainage_building_water",
        description="Urban drainage and building water flow systems",
        number_of_sites=int(500_000 * scale),
        average_unit_power_kw=0.5,        # very small unit in a drain or pipe
        capacity_factor=0.30,              # water flows intermittently
        deployment_rate_per_year=int(2_000 * scale),
        annual_growth_rate=0.08,
        efficiency_factor=0.55,
        maintenance_loss_factor=0.08,
        grid_integration_loss_factor=0.05,
        replacement_fraction_of_fossil_energy=0.60,
        manufacturing_energy_payback_years=3.0,
    )


def make_sector_irrigation(scale: float = 1.0) -> SectorConfig:
    return SectorConfig(
        name="agricultural_irrigation_canals",
        description="Agricultural irrigation channels and small canals",
        number_of_sites=int(2_000_000 * scale),
        average_unit_power_kw=2.0,
        capacity_factor=0.35,
        deployment_rate_per_year=int(5_000 * scale),
        annual_growth_rate=0.07,
        efficiency_factor=0.58,
        maintenance_loss_factor=0.10,
        grid_integration_loss_factor=0.08,
        replacement_fraction_of_fossil_energy=0.65,
        manufacturing_energy_payback_years=3.5,
    )


def make_sector_micro_hydro(scale: float = 1.0) -> SectorConfig:
    return SectorConfig(
        name="small_river_micro_hydro",
        description="Small river and micro-hydro sites",
        number_of_sites=int(300_000 * scale),
        average_unit_power_kw=10.0,
        capacity_factor=0.42,
        deployment_rate_per_year=int(1_000 * scale),
        annual_growth_rate=0.06,
        efficiency_factor=0.62,
        maintenance_loss_factor=0.08,
        grid_integration_loss_factor=0.06,
        replacement_fraction_of_fossil_energy=0.70,
        manufacturing_energy_payback_years=4.0,
    )


def make_sector_wind(scale: float = 1.0) -> SectorConfig:
    return SectorConfig(
        name="distributed_vertical_axis_wind",
        description="Distributed vertical-axis wind installations",
        number_of_sites=int(1_000_000 * scale),
        average_unit_power_kw=5.0,
        capacity_factor=0.25,              # VAWT in distributed settings often lower CF
        deployment_rate_per_year=int(3_000 * scale),
        annual_growth_rate=0.10,
        efficiency_factor=0.55,
        maintenance_loss_factor=0.10,
        grid_integration_loss_factor=0.07,
        replacement_fraction_of_fossil_energy=0.65,
        manufacturing_energy_payback_years=4.0,
    )


def make_sector_tidal(scale: float = 1.0) -> SectorConfig:
    return SectorConfig(
        name="coastal_tidal_wave_assisted",
        description="Coastal tidal and wave-assisted rotational systems",
        number_of_sites=int(50_000 * scale),
        average_unit_power_kw=20.0,
        capacity_factor=0.38,
        deployment_rate_per_year=int(500 * scale),
        annual_growth_rate=0.09,
        efficiency_factor=0.60,
        maintenance_loss_factor=0.12,      # marine environment is harder
        grid_integration_loss_factor=0.08,
        replacement_fraction_of_fossil_energy=0.70,
        manufacturing_energy_payback_years=5.0,
    )


# ---------------------------------------------------------------------------
# SCENARIO DEFINITIONS
# ---------------------------------------------------------------------------

def build_scenarios() -> List[ScenarioConfig]:
    return [
        ScenarioConfig(
            name="conservative_local_adoption",
            description=(
                "Slow adoption, small local pilots only. "
                "Illustrative lower-bound scenario. Not a forecast."
            ),
            is_stress_test=False,
            sectors=[
                make_sector_urban_drainage(scale=0.05),
                make_sector_irrigation(scale=0.05),
                make_sector_micro_hydro(scale=0.05),
                make_sector_wind(scale=0.05),
                make_sector_tidal(scale=0.05),
            ],
        ),
        ScenarioConfig(
            name="moderate_distributed_adoption",
            description=(
                "Moderate global uptake over 25 years. "
                "Illustrative mid-range scenario. Not a forecast."
            ),
            is_stress_test=False,
            sectors=[
                make_sector_urban_drainage(scale=0.20),
                make_sector_irrigation(scale=0.20),
                make_sector_micro_hydro(scale=0.20),
                make_sector_wind(scale=0.20),
                make_sector_tidal(scale=0.20),
            ],
        ),
        ScenarioConfig(
            name="accelerated_open_hardware_adoption",
            description=(
                "Rapid open-hardware replication after prototype validation. "
                "Requires successful prototyping -- not yet demonstrated. "
                "Illustrative optimistic scenario. Not a forecast."
            ),
            is_stress_test=False,
            sectors=[
                make_sector_urban_drainage(scale=0.50),
                make_sector_irrigation(scale=0.50),
                make_sector_micro_hydro(scale=0.50),
                make_sector_wind(scale=0.50),
                make_sector_tidal(scale=0.50),
            ],
        ),
        ScenarioConfig(
            name="infrastructure_integrated_adoption",
            description=(
                "Deep integration into water and infrastructure systems worldwide. "
                "Requires significant policy coordination and engineering validation. "
                "Illustrative high scenario. Not a forecast."
            ),
            is_stress_test=False,
            sectors=[
                make_sector_urban_drainage(scale=0.80),
                make_sector_irrigation(scale=0.80),
                make_sector_micro_hydro(scale=0.80),
                make_sector_wind(scale=0.80),
                make_sector_tidal(scale=0.80),
            ],
        ),
        ScenarioConfig(
            name="unrealistic_upper_bound_check",
            description=(
                "STRESS TEST ONLY -- NOT A REAL PREDICTION. "
                "Assumes 100% of all estimated sites deploy at maximum rate. "
                "This scenario is physically implausible at this scale and speed. "
                "Purpose: check model behavior at upper bound and confirm "
                "conservation-of-energy guardrails remain active."
            ),
            is_stress_test=True,
            sectors=[
                make_sector_urban_drainage(scale=1.0),
                make_sector_irrigation(scale=1.0),
                make_sector_micro_hydro(scale=1.0),
                make_sector_wind(scale=1.0),
                make_sector_tidal(scale=1.0),
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# CORE CALCULATION FUNCTIONS
# ---------------------------------------------------------------------------

def check_physical_plausibility(sector: SectorConfig) -> List[str]:
    """Return list of warning strings if assumptions exceed plausibility bounds."""
    warnings = []
    if sector.capacity_factor > MAX_PLAUSIBLE_CAPACITY_FACTOR:
        warnings.append(
            f"WARNING: capacity_factor={sector.capacity_factor:.2f} exceeds "
            f"plausible upper bound {MAX_PLAUSIBLE_CAPACITY_FACTOR:.2f} "
            f"for sector '{sector.name}'"
        )
    if sector.efficiency_factor > MAX_PLAUSIBLE_EFFICIENCY:
        warnings.append(
            f"WARNING: efficiency_factor={sector.efficiency_factor:.2f} exceeds "
            f"plausible upper bound {MAX_PLAUSIBLE_EFFICIENCY:.2f} "
            f"for sector '{sector.name}'"
        )
    if sector.average_unit_power_kw > MAX_PLAUSIBLE_UNIT_POWER_KW:
        warnings.append(
            f"WARNING: average_unit_power_kw={sector.average_unit_power_kw:.1f} exceeds "
            f"plausible upper bound {MAX_PLAUSIBLE_UNIT_POWER_KW:.1f} kW "
            f"for a small distributed unit in sector '{sector.name}'"
        )
    return warnings


def calculate_installed_capacity(
    cumulative_units: int,
    average_unit_power_kw: float,
) -> float:
    """
    Return installed capacity in GW.
    installed_capacity_gw = cumulative_units * average_unit_power_kw / 1e6
    (kW -> GW: divide by 1e6)
    """
    return cumulative_units * average_unit_power_kw / 1_000_000.0


def calculate_annual_generation(
    installed_capacity_gw: float,
    capacity_factor: float,
    efficiency_factor: float,
    maintenance_loss_factor: float,
    grid_integration_loss_factor: float,
) -> float:
    """
    Return annual electricity generation in TWh.

    Formula:
      annual_generation_twh =
          installed_capacity_gw
          * capacity_factor
          * 8760
          / 1000
          * efficiency_factor
          * (1 - maintenance_loss_factor)
          * (1 - grid_integration_loss_factor)

    Note: output is bounded by installed capacity * capacity_factor.
    Conservation of energy: efficiency_factor must be <= 1.0.
    """
    assert 0.0 <= efficiency_factor <= 1.0, "efficiency_factor must be in [0,1]"
    assert 0.0 <= capacity_factor <= 1.0, "capacity_factor must be in [0,1]"
    assert 0.0 <= maintenance_loss_factor <= 1.0
    assert 0.0 <= grid_integration_loss_factor <= 1.0

    return (
        installed_capacity_gw
        * capacity_factor
        * 8760.0
        / 1000.0
        * efficiency_factor
        * (1.0 - maintenance_loss_factor)
        * (1.0 - grid_integration_loss_factor)
    )


def calculate_avoided_emissions(
    annual_generation_twh: float,
    replacement_fraction_of_fossil_energy: float,
    fossil_grid_emission_factor_kg_per_kwh: float = FOSSIL_GRID_EMISSION_FACTOR_KG_PER_KWH,
) -> Tuple[float, float]:
    """
    Return (avoided_fossil_twh, avoided_co2_mt).

    avoided_fossil_twh = annual_generation_twh * replacement_fraction_of_fossil_energy

    avoided_co2_mt =
        avoided_fossil_twh
        * 1e9     (TWh to kWh: 1 TWh = 1e9 kWh)
        * fossil_grid_emission_factor_kg_per_kwh
        / 1e9     (kg to Mt: 1 Mt = 1e9 kg)
    """
    avoided_fossil_twh = annual_generation_twh * replacement_fraction_of_fossil_energy
    avoided_co2_mt = (
        avoided_fossil_twh
        * 1e9
        * fossil_grid_emission_factor_kg_per_kwh
        / 1e9
    )
    return avoided_fossil_twh, avoided_co2_mt


def run_scenario(scenario: ScenarioConfig) -> List[YearResult]:
    """
    Simulate year-by-year results for all sectors in a scenario.
    Returns a flat list of YearResult records.
    """
    results = []
    years = list(range(START_YEAR, END_YEAR + 1))

    for sector in scenario.sectors:
        cumulative_units = 0
        deployment_rate = sector.deployment_rate_per_year

        for year in years:
            # Grow deployment rate each year (compound growth)
            if year > START_YEAR:
                deployment_rate = deployment_rate * (1.0 + sector.annual_growth_rate)

            # Cap cumulative units at the total addressable sites
            new_units = min(int(deployment_rate), sector.number_of_sites - cumulative_units)
            new_units = max(new_units, 0)
            cumulative_units = min(cumulative_units + new_units, sector.number_of_sites)

            capacity_gw = calculate_installed_capacity(
                cumulative_units, sector.average_unit_power_kw
            )

            generation_twh = calculate_annual_generation(
                capacity_gw,
                sector.capacity_factor,
                sector.efficiency_factor,
                sector.maintenance_loss_factor,
                sector.grid_integration_loss_factor,
            )

            avoided_fossil_twh, avoided_co2_mt = calculate_avoided_emissions(
                generation_twh,
                sector.replacement_fraction_of_fossil_energy,
            )

            share_pct = (
                generation_twh / GLOBAL_ELECTRICITY_DEMAND_TWH * 100.0
                if GLOBAL_ELECTRICITY_DEMAND_TWH > 0 else 0.0
            )

            # Sensitivity: capacity factor ± 0.05
            cf_low = max(sector.capacity_factor - 0.05, 0.0)
            cf_high = min(sector.capacity_factor + 0.05, 1.0)
            gen_cf_low = calculate_annual_generation(
                capacity_gw, cf_low,
                sector.efficiency_factor,
                sector.maintenance_loss_factor,
                sector.grid_integration_loss_factor,
            )
            gen_cf_high = calculate_annual_generation(
                capacity_gw, cf_high,
                sector.efficiency_factor,
                sector.maintenance_loss_factor,
                sector.grid_integration_loss_factor,
            )

            # Sensitivity: unit power ± 30%
            cap_low = calculate_installed_capacity(
                cumulative_units, sector.average_unit_power_kw * 0.7
            )
            cap_high = calculate_installed_capacity(
                cumulative_units, sector.average_unit_power_kw * 1.3
            )
            gen_up_low = calculate_annual_generation(
                cap_low, sector.capacity_factor,
                sector.efficiency_factor,
                sector.maintenance_loss_factor,
                sector.grid_integration_loss_factor,
            )
            gen_up_high = calculate_annual_generation(
                cap_high, sector.capacity_factor,
                sector.efficiency_factor,
                sector.maintenance_loss_factor,
                sector.grid_integration_loss_factor,
            )

            warnings = check_physical_plausibility(sector)
            if scenario.is_stress_test:
                warnings.append("STRESS TEST SCENARIO -- not a real prediction")

            results.append(YearResult(
                year=year,
                sector_name=sector.name,
                cumulative_units=cumulative_units,
                installed_capacity_gw=capacity_gw,
                annual_generation_twh=generation_twh,
                avoided_fossil_twh=avoided_fossil_twh,
                avoided_co2_mt=avoided_co2_mt,
                share_of_global_electricity_pct=share_pct,
                capacity_factor_sensitivity_low_twh=gen_cf_low,
                capacity_factor_sensitivity_high_twh=gen_cf_high,
                unit_power_sensitivity_low_twh=gen_up_low,
                unit_power_sensitivity_high_twh=gen_up_high,
                warnings=warnings,
            ))

    return results


# ---------------------------------------------------------------------------
# AGGREGATION HELPERS
# ---------------------------------------------------------------------------

def aggregate_by_year(results: List[YearResult]) -> Dict[int, dict]:
    """Sum all sectors per year."""
    agg = {}
    for r in results:
        if r.year not in agg:
            agg[r.year] = {
                "installed_capacity_gw": 0.0,
                "annual_generation_twh": 0.0,
                "avoided_fossil_twh": 0.0,
                "avoided_co2_mt": 0.0,
                "share_of_global_electricity_pct": 0.0,
            }
        agg[r.year]["installed_capacity_gw"] += r.installed_capacity_gw
        agg[r.year]["annual_generation_twh"] += r.annual_generation_twh
        agg[r.year]["avoided_fossil_twh"] += r.avoided_fossil_twh
        agg[r.year]["avoided_co2_mt"] += r.avoided_co2_mt
        agg[r.year]["share_of_global_electricity_pct"] += r.share_of_global_electricity_pct
    return agg


# ---------------------------------------------------------------------------
# OUTPUT FUNCTIONS
# ---------------------------------------------------------------------------

def write_csv(all_scenario_results: Dict[str, List[YearResult]]) -> str:
    """Write all results to CSV. Returns the file path."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    filepath = os.path.join(RESULTS_DIR, "global_adoption_scenario.csv")

    fieldnames = [
        "scenario",
        "year",
        "sector",
        "cumulative_units",
        "installed_capacity_gw",
        "annual_generation_twh",
        "avoided_fossil_twh",
        "avoided_co2_mt",
        "share_of_global_electricity_pct",
        "cf_sensitivity_low_twh",
        "cf_sensitivity_high_twh",
        "unit_power_sensitivity_low_twh",
        "unit_power_sensitivity_high_twh",
        "warnings",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for scenario_name, results in all_scenario_results.items():
            for r in results:
                writer.writerow({
                    "scenario": scenario_name,
                    "year": r.year,
                    "sector": r.sector_name,
                    "cumulative_units": r.cumulative_units,
                    "installed_capacity_gw": f"{r.installed_capacity_gw:.6f}",
                    "annual_generation_twh": f"{r.annual_generation_twh:.6f}",
                    "avoided_fossil_twh": f"{r.avoided_fossil_twh:.6f}",
                    "avoided_co2_mt": f"{r.avoided_co2_mt:.4f}",
                    "share_of_global_electricity_pct": f"{r.share_of_global_electricity_pct:.6f}",
                    "cf_sensitivity_low_twh": f"{r.capacity_factor_sensitivity_low_twh:.6f}",
                    "cf_sensitivity_high_twh": f"{r.capacity_factor_sensitivity_high_twh:.6f}",
                    "unit_power_sensitivity_low_twh": f"{r.unit_power_sensitivity_low_twh:.6f}",
                    "unit_power_sensitivity_high_twh": f"{r.unit_power_sensitivity_high_twh:.6f}",
                    "warnings": "; ".join(r.warnings),
                })

    return filepath


def print_summary_table(all_scenario_results: Dict[str, List[YearResult]]) -> None:
    """Print ASCII summary table to console."""
    milestone_years = [2026, 2030, 2035, 2040, 2045, 2050]

    header = (
        "GLOBAL ADOPTION SCENARIO SIMULATOR\n"
        "Dual-Core Edge Magnetic Structure for Universal Rotational Energy Harvesting\n"
        "\n"
        "DISCLAIMER: Scenario model only. Illustrative assumptions. Not a forecast.\n"
        "            No physical prototype validated. Not a claim of free energy.\n"
        "            Output bounded by available mechanical input minus losses.\n"
    )
    print(header)

    col_w = [30, 6, 10, 10, 12, 12, 14]
    sep = "+" + "+".join("-" * w for w in col_w) + "+"
    row_fmt = "|" + "|".join("{:>" + str(w) + "}" for w in col_w) + "|"

    for scenario_name, results in all_scenario_results.items():
        scenarios_list = build_scenarios()
        scenario_obj = next((s for s in scenarios_list if s.name == scenario_name), None)
        stress_flag = " [STRESS TEST]" if (scenario_obj and scenario_obj.is_stress_test) else ""

        print(sep)
        label = f" Scenario: {scenario_name}{stress_flag} "
        print("|" + label.ljust(sum(col_w) + len(col_w) - 1) + "|")
        if scenario_obj:
            desc_lines = _wrap(scenario_obj.description, sum(col_w) + len(col_w) - 1)
            for line in desc_lines:
                print("|" + (" " + line).ljust(sum(col_w) + len(col_w) - 1) + "|")
        print(sep)
        print(row_fmt.format(
            "Year", "Cap.", "Gen.", "Fossil", "CO2 avd.", "Share %",
            "CF sens. lo/hi"
        ))
        print(row_fmt.format(
            "", "GW", "TWh", "TWh", "Mt CO2", "global elec.",
            "TWh"
        ))
        print(sep)

        agg = aggregate_by_year(results)
        # Collect per-year CF sensitivity totals
        cf_by_year: Dict[int, Tuple[float, float]] = {}
        for r in results:
            y = r.year
            lo, hi = cf_by_year.get(y, (0.0, 0.0))
            cf_by_year[y] = (
                lo + r.capacity_factor_sensitivity_low_twh,
                hi + r.capacity_factor_sensitivity_high_twh,
            )

        for year in milestone_years:
            if year not in agg:
                continue
            d = agg[year]
            cf_lo, cf_hi = cf_by_year.get(year, (0.0, 0.0))
            cf_str = f"{cf_lo:.2f}/{cf_hi:.2f}"
            print(row_fmt.format(
                str(year),
                f"{d['installed_capacity_gw']:.3f}",
                f"{d['annual_generation_twh']:.3f}",
                f"{d['avoided_fossil_twh']:.3f}",
                f"{d['avoided_co2_mt']:.3f}",
                f"{d['share_of_global_electricity_pct']:.4f}%",
                cf_str,
            ))

        print(sep)
        print()

    # Collect and print any warnings
    all_warnings = set()
    for results in all_scenario_results.values():
        for r in results:
            for w in r.warnings:
                all_warnings.add(w)

    if all_warnings:
        print("=== PHYSICAL PLAUSIBILITY WARNINGS ===")
        for w in sorted(all_warnings):
            print(f"  {w}")
        print()


def _wrap(text: str, width: int) -> List[str]:
    """Naive word-wrap for console output."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


# ---------------------------------------------------------------------------
# OPTIONAL PLOTTING
# ---------------------------------------------------------------------------

def plot_results(all_scenario_results: Dict[str, List[YearResult]]) -> None:
    """Generate PNG plots if matplotlib is available. Silently skips if not."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed -- skipping plots. CSV and console output still produced.")
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)
    years = list(range(START_YEAR, END_YEAR + 1))

    # --- Plot 1: Annual generation by sector (moderate scenario) ---
    target_scenario = "moderate_distributed_adoption"
    if target_scenario in all_scenario_results:
        results = all_scenario_results[target_scenario]
        sectors = list({r.sector_name for r in results})
        fig, ax = plt.subplots(figsize=(12, 6))
        for sector_name in sectors:
            sector_results = [r for r in results if r.sector_name == sector_name]
            sector_results.sort(key=lambda r: r.year)
            ys = [r.annual_generation_twh for r in sector_results]
            ax.plot(years, ys, label=sector_name.replace("_", " "))
        ax.set_title(
            "Annual Generation by Sector\n"
            f"Scenario: {target_scenario}\n"
            "[ILLUSTRATIVE -- not measured hardware performance]",
            fontsize=10
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Annual Generation (TWh)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        path = os.path.join(RESULTS_DIR, "global_energy_contribution_by_sector.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"  Plot saved: {path}")

    # --- Plot 2: Fossil replacement potential across scenarios ---
    fig, ax = plt.subplots(figsize=(12, 6))
    for scenario_name, results in all_scenario_results.items():
        agg = aggregate_by_year(results)
        ys = [agg[y]["avoided_fossil_twh"] for y in years if y in agg]
        label = scenario_name.replace("_", " ")
        style = "--" if "unrealistic" in scenario_name else "-"
        ax.plot(years[:len(ys)], ys, label=label, linestyle=style)
    ax.set_title(
        "Fossil Replacement Potential Across Scenarios\n"
        "[ILLUSTRATIVE -- scenario model, not a forecast]",
        fontsize=10
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Avoided Fossil Electricity (TWh)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(RESULTS_DIR, "fossil_replacement_potential.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Plot saved: {path}")

    # --- Plot 3: Adoption growth curve (installed capacity) ---
    fig, ax = plt.subplots(figsize=(12, 6))
    for scenario_name, results in all_scenario_results.items():
        agg = aggregate_by_year(results)
        ys = [agg[y]["installed_capacity_gw"] for y in years if y in agg]
        label = scenario_name.replace("_", " ")
        style = "--" if "unrealistic" in scenario_name else "-"
        ax.plot(years[:len(ys)], ys, label=label, linestyle=style)
    ax.set_title(
        "Adoption Growth Curve -- Installed Capacity\n"
        "[ILLUSTRATIVE -- scenario model, not a forecast]",
        fontsize=10
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Installed Capacity (GW)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(RESULTS_DIR, "adoption_growth_curve.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Plot saved: {path}")


# ---------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------

def main() -> None:
    print("Running Global Adoption Scenario Simulator...")
    print("(Scenario model -- illustrative assumptions -- not a forecast)\n")

    scenarios = build_scenarios()
    all_results: Dict[str, List[YearResult]] = {}

    for scenario in scenarios:
        results = run_scenario(scenario)
        all_results[scenario.name] = results

    print_summary_table(all_results)

    csv_path = write_csv(all_results)
    print(f"CSV written: {csv_path}\n")

    print("Generating optional plots...")
    plot_results(all_results)

    print("\nDone.")
    print(
        "\nREMINDER: All numbers are illustrative assumptions based on no measured "
        "hardware performance.\nPhysical prototype validation is required before "
        "any real-world claims can be made."
    )


if __name__ == "__main__":
    main()
