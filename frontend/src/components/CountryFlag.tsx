"use client";

import Image from "next/image";
import ReactCountryFlag from "react-country-flag";
import { countryCodeMap } from "@/lib/country-code-map";
import { nationalityToFlagCode } from "@/lib/nationality-to-flag-code";

export function CountryFlag({
  country,
  nationality,
  ...props
}: {
  country?: string;
  nationality?: string;
  className?: string;
  [key: string]: unknown;
}) {
  // 方案一：根据国籍，使用 react-country-flag 库 (用于车手)
  if (nationality) {
    const countryCode = nationalityToFlagCode[nationality];
    if (!countryCode) return null; // or a placeholder

    return (
      <ReactCountryFlag
        countryCode={countryCode}
        svg
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
        title={nationality}
        {...props}
      />
    );
  }

  // 方案二：根据国家/地点，使用本地的 SVG 文件 (用于赛历)
  if (country) {
    const countryCode = countryCodeMap[country];
    if (!countryCode) return null; // or a placeholder

    return (
      <Image
        src={`/country_flags/${countryCode.toUpperCase()}.svg`}
        alt={`${country} flag`}
        title={country}
        width={20}
        height={15}
        {...props}
      />
    );
  }

  return null;
}
