# DataBursatil API v2 Research Notes

## Overview

DataBursatil API is currently on version 2 (`/v2/`). The previous version (`/v1/`) is obsolete.

**Documentation**: <https://www.databursatil.com/docs.html>  
**Status page**: <https://status.databursatil.com>

## Authentication

Auth is via a **token query parameter** (`?token=...`). No headers, no OAuth.

- Token is a 30-character alphanumeric string
- Obtained from the DataBursatil dashboard after login
- Stored in `BMV_API_TOKEN` environment variable

## Endpoints Used

### `/v2/cotizaciones` (Quotes)

| Parameter     | Required | Description |
|---------------|----------|-------------|
| `token`       | Yes      | Auth token  |
| `emisora_serie` | Yes    | Ticker with series (e.g. `GFNORTEO`, `WALMEX*`). Up to 50, comma-separated |
| `concepto`    | Yes      | Price fields: `u,p,a,x,n,c,m,v,o,i` |
| `bolsa`       | Yes      | Exchange: `BMV` and/or `BIVA` |

**Response**: `{SYMBOL: {bmv: {u, p, a, x, n, c, m, v, o, i, f}, biva: {...}}}`

Concepts: `u`=ultimo, `p`=ppp, `a`=anterior, `x`=maximo, `n`=minimo, `c`=cambio%, `m`=cambio$, `v`=volumen, `o`=operaciones, `i`=importe, `f`=fecha

### `/v2/divisas` (Currencies)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token`   | Yes      | Auth token  |
| `ticker`  | No       | Filter by currency pair (e.g. `USDMXN,EURMXN`) |

**Response**: `{PAIR: {u, c, m}, ..., "t": "YYYY-MM-DD HH:MM:SS"}`

Fields: `u`=rate, `c`=change%, `m`=change$, `f`=fecha

### `/v2/creditos` (Credits)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token`   | Yes      | Auth token  |

**Response**: `{"disponibles": "249458"}`

200,000 credits/month. 1 credit per KiB of response data.

### `/v2/emisoras` (Search / Dividends)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token`   | Yes      | Auth token  |
| `letra`   | No       | Filter by letter or ticker name |
| `mercado` | No       | `local` and/or `global` |

**Response**: `{SYMBOL: {SERIE: {razon_social, isin, bolsa, tipo_valor_descripcion, estatus, acciones_en_circulacion, dividendos: {reciente: {...}, historico: {...}}}}}`

**Important**: `letra` searches by emitter name, not full ticker+series. When user passes `FMTY14`, must extract `FMTY` before querying.

## Key Findings

1. **No breaking auth changes** - token query parameter still works, `BMV_API_TOKEN` env var unchanged
2. **Endpoints use `/v2/`** - same base URL structure as before
3. **Response format** is JSON, nested by exchange for `cotizaciones`, flat for `divisas`
4. **`emisoras` endpoint** serves dual purpose: search by letter AND dividend info (via `dividendos` field)
5. **Series suffix handling** - tickers include series (e.g. `GFNORTEO` = GFNORTE + series O, `FMTY14` = FMTY + series 14)
6. **Credits are generous** - 200k/month, ~1 credit per KiB response
