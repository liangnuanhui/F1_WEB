/**
 * A set containing the base names of all available driver avatars.
 * This is used to proactively check if an avatar exists before attempting to load it,
 * preventing 404 errors in the console.
 * The names are without file extensions.
 */
export const availableAvatarSet = new Set([
  "Alexander_Albon",
  "Andrea_Kimi_Antonelli",
  "Carlos_Sainz",
  "Charles_Leclerc",
  "Esteban_Ocon",
  "Fernando_Alonso",
  "Franco_Colapinto",
  "Gabriel_Bortoleto",
  "George_Russell",
  "Isack_Hadjar",
  "Lance_Stroll",
  "Lando_Norris",
  "Lewis_Hamilton",
  "Liam_Lawson",
  "Max_Verstappen",
  "Nico_Hulkenberg",
  "Oliver_Bearman",
  "Oscar_Piastri",
  "Pierre_Gasly",
  "Yuki_Tsunoda",
]);
