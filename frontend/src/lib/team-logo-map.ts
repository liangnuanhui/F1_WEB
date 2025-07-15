/**
 * F1 Team Logo Filename Map
 *
 * This file maps the `constructor_id` from the database to the specific
 * filename of the team's logo SVG in the `/public/team_logos` directory.
 * This is necessary because constructor IDs do not always directly correspond
 * to the logo filenames.
 */

export const teamLogoMap: Record<string, string> = {
  alpine: "alpine",
  aston_martin: "aston-martin",
  ferrari: "ferrari",
  haas: "haas-f1-team",
  sauber: "kick-sauber", // Sauber is Kick Sauber
  mclaren: "mclaren",
  mercedes: "mercedes",
  rb: "racing-bulls", // RB F1 Team is Racing Bulls
  red_bull: "red-bull-racing",
  williams: "williams",
};

/**
 * A utility function to safely get a team's logo filename.
 * It uses the map to find the correct filename for a given constructorId.
 * @param constructorId - The constructor_id of the team.
 * @returns The logo filename (without extension).
 */
export const getTeamLogoFilename = (constructorId: string): string => {
  const lowerId = constructorId.toLowerCase();
  return teamLogoMap[lowerId] || lowerId; // Fallback to the id itself
};
