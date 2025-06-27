"use client";

import { getFlagCodeByNationality } from "@/lib/utils";
import ReactCountryFlag from "react-country-flag";

interface CountryFlagProps {
  nationality: string;
  className?: string;
}

export function CountryFlag({ nationality, className }: CountryFlagProps) {
  const countryCode = getFlagCodeByNationality(nationality);

  if (!countryCode) {
    return null; // Or a placeholder for missing flags
  }

  return (
    <ReactCountryFlag
      countryCode={countryCode}
      svg
      className={className}
      title={nationality}
      style={{
        width: "100%",
        height: "100%",
      }}
    />
  );
}
