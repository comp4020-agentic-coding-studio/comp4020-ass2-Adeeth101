declare module "virtual:astro-theme-university/fonts" {
  type CourseFont = "--font-public-sans" | "--font-roboto-mono";
  export const fontVariables: CourseFont[];
  export const preloadFontVariables: CourseFont[];
}

declare module "virtual:astro-theme-university/llms" {
  export const llmsTxtHref: string | null;
}
