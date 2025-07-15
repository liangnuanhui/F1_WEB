/**
 * F1 Team Colors
 *
 * This file contains the official theme colors for the Formula 1 teams,
 * indexed by their `constructor_id`. These colors are used throughout the
 * frontend for consistent branding in UI components like charts, borders,
 * and backgrounds.
 *
 * The colors are stored here as a frontend concern to separate display logic
 * from backend data.
 */

export const teamColors: Record<string, string> = {
  alpine: "rgb(0, 161, 232)",
  aston_martin: "rgb(34, 153, 113)",
  ferrari: "rgb(237, 17, 49)",
  haas: "rgb(156, 159, 162)",
  mclaren: "rgb(244, 118, 0)",
  mercedes: "rgb(0, 215, 182)",
  rb: "rgb(108, 152, 255)",
  red_bull: "rgb(71, 129, 215)",
  sauber: "rgb(1, 192, 14)",
  williams: "rgb(24, 104, 219)",
  // Add a default color for teams not in the list
  default: "rgb(128, 128, 128)", // Gray
};

/**
 * A utility function to safely get a team's color.
 * Falls back to a default color if the team ID is not found.
 * @param constructorId - The constructor_id of the team.
 * @returns The RGB color string for the team.
 */
export const getTeamColor = (constructorId?: string): string => {
  if (!constructorId) {
    return teamColors.default;
  }
  return teamColors[constructorId.toLowerCase()] || teamColors.default;
};
