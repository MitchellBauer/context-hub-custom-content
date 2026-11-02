---
name: zebrash-go
description: "zebrash guide for rendering ZPL labels to PNG previews in Go"
metadata:
  languages: "go"
  versions: "1.38.0"
  revision: 1
  updated-on: "2026-11-01"
  source: community
  tags: "zebrash,zpl,zebra,label,preview,png,go"
---

# zebrash for Go

`github.com/ingridhq/zebrash` parses ZPL (Zebra Programming Language) and draws
each label as a raster image, with no Zebra printer and no third-party service
(Labelary-style, self-hosted). Pure Go, so no CGO.

It emulates a **subset** of ZPL. Use it for a preview of what a label should
look like. A real print on the real printer is the final word.

## Basic use

```go
import (
    "bytes"

    "github.com/ingridhq/zebrash"
    "github.com/ingridhq/zebrash/drawers"
)

func previewPNG(zpl []byte) ([]byte, error) {
    labels, err := zebrash.NewParser().Parse(zpl) // one entry per ^XA...^XZ
    if err != nil {
        return nil, err
    }
    var buf bytes.Buffer
    err = zebrash.NewDrawer().DrawLabelAsPng(labels[0], &buf, drawers.DrawerOptions{
        LabelWidthMm:    101.6, // 4 in
        LabelHeightMm:   152.4, // 6 in
        Dpmm:            8,     // 203 dpi
        GrayscaleOutput: true,
    })
    return buf.Bytes(), err
}
```

- `Parse` returns a slice: a template with two `^XA...^XZ` blocks yields two
  labels. Draw each one; join them yourself if you want a set side by side.
- Check `len(labels) > 0` before indexing. A template with no label content
  gives an empty slice.

## DrawerOptions

| Field | Meaning |
| --- | --- |
| `LabelWidthMm`, `LabelHeightMm` | Label size in millimetres. Convert inches with `* 25.4`. |
| `Dpmm` | Dots per mm. 6 = 152 dpi, 8 = 203 dpi, 12 = 300 dpi, 24 = 600 dpi. |
| `GrayscaleOutput` | Gray PNG instead of RGBA. Smaller files. |
| `EnableInvertedLabels` | Honor `^POI` (inverted orientation). |

Map printer dpi to `Dpmm` by rounding `dpi / 25.4` (203 -> 8, 300 -> 12).
Always pass width and height yourself rather than relying on the ZPL to size
the image.

## Supported commands (v1.38.0)

Formats: `^XA` `^XZ` `^XF` `^XG` `^DF` `~DG` `~DU`.
Fields: `^FO` `^FT` `^FD` `^FV` `^FN` `^FS` `^FB` `^FH` `^FR` `^FW`.
Fonts: `^A` `^CF` `^CI` `^CW`.
Barcodes: `^BY` `^BC` (Code 128) `^B3` (Code 39) `^BE` (EAN-13) `^B2`
(Interleaved 2 of 5) `^B7` (PDF417) `^BQ` (QR) `^BX` (DataMatrix) `^BO` (Aztec)
`^BD` (MaxiCode).
Graphics: `^GB` `^GC` `^GD` `^GF` `^GS` (symbols).
Layout: `^LH` `^LR` `^PO` `^PW` `^IL`.

Anything else is ignored rather than rendered. Do not expect a preview to show
the effect of print quantity (`^PQ`), darkness, media settings or sensors.

## Gotchas

- **Fonts.** Zebra's resident fonts are approximated with embedded fonts, so
  text widths and wrapping can differ a little from the printer. Leave
  margin in the layout rather than matching the preview pixel for pixel.
- **Hex escapes.** `^FH` plus `_xx` escapes in field data are decoded; the
  default indicator is `_`. Escape user data (see the `zpl-labels` entry).
- **QR data.** For `^BQ`, field data starts with the error-correction letter
  and `A` for automatic input (`^FDQA,payload^FS`). Make sure the preview of
  your QR matches what a scanner reads from the printed label.
- **Rotation.** `^A0R`, `^FWR` and `^POI` are drawn, but verify rotated
  layouts on a real label the first time.
- **Untrusted ZPL.** Parsing and drawing allocate by label and image size.
  Cap the size of ZPL you accept and the dimensions you pass in.

## Related entries

- `zpl-labels`: ZPL language notes, escaping and safe templating.
