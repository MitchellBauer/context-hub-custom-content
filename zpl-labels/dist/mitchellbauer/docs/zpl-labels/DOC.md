---
name: zpl-labels
description: "ZPL II notes for generating Zebra labels from Go templates: structure, fields, barcodes, escaping, safety"
metadata:
  languages: "go"
  versions: "1.0.0"
  revision: 1
  updated-on: "2026-11-01"
  source: community
  tags: "zpl,zebra,label,barcode,qr,code128,printer,text-template,go"
---

# ZPL II for generated labels

ZPL (Zebra Programming Language) is a stream of commands. Each starts with `^`
(format commands) or `~` (control commands) followed by a two-character name
and comma-separated parameters. Whitespace and newlines between commands are
ignored. This entry covers what you need to generate label content from Go
(`text/template`) and keep it safe.

Preview with `zebrash-go`. Verify on the real printer; the preview is a subset.

## Format skeleton

```zpl
^XA                      start of one label
^CI28                    UTF-8 for field data
^FO50,40^A0N,60,60^FB700,1,0,L^FH^FDHello^FS
^FO50,160^BY3^BCN,120,N,N,N^FH^FD12345^FS
^FO50,320^BQN,2,8^FH^FDQA,S1000,SKU,LOT,10^FS
^XZ                      end of label
```

## Core commands

| Command | Meaning |
| --- | --- |
| `^XA` / `^XZ` | Begin / end a label format. Each pair prints one label. |
| `^FOx,y` | Field origin: top-left corner of the next field, in dots. |
| `^FTx,y` | Field typeset: baseline origin (text sits on y). |
| `^FD...^FS` | Field data, terminated by `^FS`. |
| `^FX text` | Comment. Ends at the next `^` or `~`, so never write those in it. |
| `^A0N,h,w` | Scalable font 0, orientation, height and width in dots. |
| `^CFf,h,w` | Default font. |
| `^CI28` | Character set. 28 = UTF-8. |
| `^FBw,lines,spacing,just` | Field block: wrap in `w` dots, max lines, justify `L C R J`. |
| `^FH` | Enable `_xx` hex escapes in the field's data (default indicator `_`). |
| `^FR` | Field reverse print (inverts against what is underneath). |
| `^GBw,h,t` | Graphic box or line, `t` = border thickness in dots. |
| `^PQq` | Print quantity (copies). |

Orientations: `N` normal, `R` rotated 90 clockwise, `I` inverted 180, `B` read from bottom (270).

## Dots and sizes

Dots = inches x dpi. At **203 dpi** (8 dots/mm) a 4x6 label is 812 x 1218 dots;
at 300 dpi it is 1200 x 1800. Design in dots and note the dpi in the file name
or header comment (for example `roll-usage-4x6-203.zpl`).

## Barcodes

Set module width once with `^BYw` (w = narrow bar width in dots), then:

| Command | Barcode |
| --- | --- |
| `^BCo,h,f,g,e` | Code 128. `h` height, `f` print text (`Y/N`), `g` text above (`Y/N`), `e` UCC check (`N`). |
| `^B3o,e,h,f,g` | Code 39. |
| `^BQo,model,mag,ec,mask` | QR. Use model `2`, magnification 1-10, e.g. `^BQN,2,8`. |
| `^BXo,h,q,...` | DataMatrix. |
| `^B7` | PDF417. |

- QR field data starts with the error-correction level and `A` for automatic
  mode: `^FDQA,payload^FS` (Q = 25% recovery; H, M, L also valid). That
  prefix is not part of what a scanner reads.
- QR size = modules x magnification dots. A version-3 code (29 modules) at
  magnification 13 is 377 dots, about 1.86 in at 203 dpi. Check the
  physical size against the requirement.
- Code 128 needs a quiet zone (about 10x module width) each side. Barcode
  width grows with data length; reduce `^BY` or move to a rotated layout for
  long values.
- Barcode and text sizes interact with `^FB` wrapping; leave headroom.

## Escaping field data

`^` and `~` in data would start a new command. Enable `^FH` on the field and
hex-escape those characters (and anything else the printer must not interpret):

```go
func esc(s string) string {
    var b strings.Builder
    for _, r := range s {
        if r == '^' || r == '~' || r == '_' || r < 0x20 || r > 0x7e {
            for _, by := range []byte(string(r)) { // UTF-8 bytes
                fmt.Fprintf(&b, "_%02X", by)
            }
            continue
        }
        b.WriteRune(r)
    }
    return b.String()
}
```

- Escape `_` too, because it is the hex indicator.
- With `^CI28`, `^FH` bytes are UTF-8, so a multi-byte character becomes
  several `_xx` pairs.
- Every field that prints user data needs both `^FH` and escaped values.
  Register the helper as a template function (`template.FuncMap{"esc": esc}`)
  and call `{{esc .Value}}` in the template.

## Templating from Go

```zpl
^FO612,20^A0R,{{if le (len .SKU) 9}}180,145{{else}}120,82{{end}}^FB750,1,0,L^FH^FD{{esc .SKU}}^FS
```

- Use `text/template` for ZPL, not `html/template` (which would HTML-escape).
- Choose font size by value length so long SKUs do not overflow.
- Do not put template actions inside `^FX` comments if the values could
  contain `^` or `~`.

## Printer settings belong to the printer

Exports from label designers often prepend commands that rewrite the printer
configuration and save it. Generated labels should contain **content only**:

- Safe (label content): `^XA ^XZ`, `^F*` fields, `^A*` fonts, `^CF ^CI ^CW`,
  `^B*` barcodes, `^G*` graphics, `^XG ^IM ~DG ~DY`, `^PQ`, `^PA`, `^SN ^SF`.
- Settings that should be dropped: `^PW ^LL ^LH ^LT ^LS ^MT ^MN ^MM ^MD ~SD
  ^PR ^PO ^PM ^LR ^JU ^JM ~TA ~JS ~JC`, network and sensor settings, SGD
  commands (`! U1 setvar ...`), and anything that saves with `^JUS`.
- `^CC ~CC ^CT ~CT ^CD ~CD` change the command prefix characters, which makes
  the rest of the stream unparseable. Refuse templates that use them. The
  designer header `CT~~CD,~CC^~CT~` just restates defaults and can be removed.

Filter templates against an allowlist before sending, split the stream on
`^` and `~`, and drop empty formats (a settings-only `^XA...^XZ` block would
feed a blank label).

## Sending to the printer

- Raw TCP to port **9100** on the printer's IP: write the ZPL bytes, close
  the connection. No framing or reply is needed.
- Set a dial and write deadline; printers go offline.
- One connection can carry several `^XA...^XZ` blocks (a set of labels).

## Debug checklist

1. Blank label: no fields, or a settings-only format dropped.
2. Text cut off: `^FB` width or field origin outside the label.
3. QR will not scan: too small (low magnification), no quiet zone, or the
   `QA,` prefix is missing.
4. Characters wrong: missing `^CI28` or `^FH`/escape mismatch.
5. Everything shifted after a template change: a stray `^LH` or `^PW` in the
   file; remove printer-setting commands.
