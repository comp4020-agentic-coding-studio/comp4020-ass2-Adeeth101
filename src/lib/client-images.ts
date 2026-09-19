import type { ImageMetadata } from "astro";
import adelaide from "../assets/images/client-adelaide.jpg";
import aliceSprings from "../assets/images/client-alice-springs.jpg";
import brisbane from "../assets/images/client-brisbane.jpg";
import canberra from "../assets/images/client-canberra.jpg";
import darwin from "../assets/images/client-darwin.jpg";

export const clientImages: Record<string, ImageMetadata> = {
  adelaide,
  "alice-springs": aliceSprings,
  brisbane,
  canberra,
  darwin,
};

export const clientImageAlt: Record<string, string> = {
  adelaide: "Illustration of a single-storey double-brick suburban house and front garden.",
  "alice-springs": "Illustration of a low blockwork house on an arid rural property.",
  brisbane: "Illustration of attached two-storey townhouses with compact courtyards.",
  canberra: "Illustration of a brick-veneer suburban house among mature eucalypts.",
  darwin: "Illustration of an elevated steel-frame tropical house beneath storm clouds.",
};
