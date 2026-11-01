# Run folders, as the lab machine saw them on 01 November 2026, 22:26 (IST)

Written by `scripts/sync.py` from local files only. A started run is fetched when it ends; until then its state on the GPU is read with `cl/gcp_run.py status RUN`.

## Started and not yet fetched (10)
| Run | Machine | Started | Hours allowed |
| --- | --- | --- | --- |
| `runs/aca-dev/w9792-s2` | Azure Container Apps serverless A100 | 2026-10-27 18:57:56 | 20.0 |
| `runs/bl1-dev-1.5b/w9792-alphaedit` | Azure Container Apps serverless T4 | 2026-10-27 20:33:40 | 6.0 |
| `runs/bl1-dev-1.5b/w9792-alphaedit-r2` | Azure Container Apps serverless T4 | 2026-10-27 20:39:34 | 6.0 |
| `runs/ccl6-main-72b/w9708` | Google Cloud Vertex AI A100-2X (Spot, us-central1) | 2026-11-01 00:22:23 | 20.0 |
| `runs/ccl6-main-72b/w9709` | Google Cloud Vertex AI A100-2X (Spot, us-central1) | 2026-11-01 12:37:37 | 20.0 |
| `runs/ccl7-dev-1.5b/w9792-v11` | Google Cloud Vertex AI A100 (Spot, europe-west4) | 2026-11-01 15:03:03 | 20.0 |
| `runs/ccl7-dev-7b/w9792-v11` | Google Cloud Vertex AI A100 (Spot, us-central1) | 2026-11-01 15:02:28 | 20.0 |
| `runs/tx1-dev/w9792-learn7b-v6` | Google Cloud Vertex AI A100 (Spot, europe-west4) | 2026-10-31 22:55:57 | 20.0 |
| `runs/x10-main-7b/w9724` | Google Cloud Vertex AI A100 (Spot, europe-west4) | 2026-11-01 01:12:00 | 20.0 |
| `runs/xf2-main-olmoe/w9702` | Google Cloud Vertex AI A100 (Spot, us-central1) | 2026-11-01 01:08:59 | 20.0 |

## Packed, not started (40)
| Run |
| --- |
| `runs/bc1-dev-1.5b/w9792-v5` |
| `runs/bl1-main-7b/stats` |
| `runs/bl1-main-7b/w9702-alphaedit` |
| `runs/bl1-main-7b/w9702-memit` |
| `runs/bl1-main-7b/w9703-alphaedit` |
| `runs/bl1-main-7b/w9703-memit` |
| `runs/ccl1-dev-20261024/w9590` |
| `runs/ccl2-tpu72w-dev-20261024/w9790` |
| `runs/ccl2-tpu72x-dev-20261025/w9790` |
| `runs/ccl3-main-20261025/w9702` |
| `runs/ccl3-main-20261025/w9703` |
| `runs/ccl4-main-72b/w9702` |
| `runs/ccl4-main-72b/w9703` |
| `runs/ccl4-main-7b/w9702` |
| `runs/ccl4-main-7b/w9703` |
| `runs/ccl4c72-main-72b/w9714-errors` |
| `runs/ccl4c72-main-72b/w9714-retrain` |
| `runs/ccl4c72-main-72b/w9715-errors` |
| `runs/ccl4c72-main-72b/w9715-retrain` |
| `runs/ccl4c72-main-72b/w9716-errors` |
| `runs/ccl4c72-main-72b/w9716-retrain` |
| `runs/ccl4c72-main-72b/w9717-errors` |
| `runs/ccl4c72-main-72b/w9717-retrain` |
| `runs/ccl4r-7b/w9704` |
| `runs/ccl4r-7b/w9705` |
| `runs/ccl7-dev-1.5b/w9792-v2-r2` |
| `runs/clx15-72b-speed-20261026/w9792` |
| `runs/clx3-20261025/w9790` |
| `runs/clxt1-20261025/w9790` |
| `runs/clxt2-20261025/w9790` |
| `runs/clxt3-20261025/w9791` |
| `runs/dr1-dev-1.5b/w9792-delete` |
| `runs/dr1-dev-1.5b/w9792-retrain` |
| `runs/ke1-dev-20261024/failed1-w9490` |
| `runs/ke1-dev-20261024/w9490` |
| `runs/rg1-dev-7b/w9792` |
| `runs/xfm-main-gemma/w9702` |
| `runs/xfm-main-gemma/w9703` |
| `runs/xfm-main-llama/w9702` |
| `runs/xfm-main-llama/w9703` |

## Ended without a done line (6)
| Run | State |
| --- | --- |
| `runs/bl1-dev-1.5b/w9792-memit` | exit code 1, no done line |
| `runs/bl1-dev-1.5b/w9792-memit-r4` | exit code 1, no done line |
| `runs/ccl7-dev-1.5b/w9792-v2` | exit code 143, no done line |
| `runs/wb1-dev-7b/w9792-v6` | exit code 1, no done line |
| `runs/xfm-main-phi/w9702` | exit code 1, no done line |
| `runs/xfm-main-phi/w9703` | exit code 1, no done line |

## Done (109)
| Run | State |
| --- | --- |
| `runs/aca-dev/w9792-s2b` | exit code 0 |
| `runs/bc1-dev/w9792-v6` | exit code 0 |
| `runs/bc1-dev/w9792-v7-r2` | exit code 0 |
| `runs/bc1-dev-1.5b/w9792-v6` | exit code 0 |
| `runs/bc1-dev-1.5b/w9792-v8-r2` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-alphaedit-r3` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-alphaedit-r5` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-alphaedit-r6-plain` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-memit-r3` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-memit-r5` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-memit-r6-plain` | exit code 0 |
| `runs/bl1-dev-1.5b/w9792-stats` | exit code 0 |
| `runs/bl2-dev-7b/w9792` | exit code 0 |
| `runs/bl2-main-7b/w9702` | exit code 0 |
| `runs/bl2-main-7b/w9703` | exit code 0 |
| `runs/bl3-main-7b/w9702` | exit code 0 |
| `runs/bl3-main-7b/w9703` | exit code 0 |
| `runs/ccl2-dev2-20261024/w9790` | exit code ? |
| `runs/ccl2-dev3-20261024/w9790` | exit code ? |
| `runs/ccl2-main-20261025/w9700` | exit code ? |
| `runs/ccl2-main-20261025/w9701` | exit code ? |
| `runs/ccl2h-gpt41-dev3-20261025/w9790` | exit code ? |
| `runs/ccl4-main-7b-colab/w9703` | exit code 0 |
| `runs/ccl4c-dev-7b/w9704-retrain` | exit code 0 |
| `runs/ccl4c-main-7b/w9714-errors` | exit code 0 |
| `runs/ccl4c-main-7b/w9714-retrain` | exit code 0 |
| `runs/ccl4c-main-7b/w9715-errors` | exit code 0 |
| `runs/ccl4c-main-7b/w9715-retrain` | exit code 0 |
| `runs/ccl4c-main-7b/w9716-errors` | exit code 0 |
| `runs/ccl4c-main-7b/w9716-retrain` | exit code 0 |
| `runs/ccl4c-main-7b/w9717-errors` | exit code 0 |
| `runs/ccl4c-main-7b/w9717-retrain` | exit code 0 |
| `runs/ccl4c72-dev-72b/w9792-errors-s4` | exit code 0 |
| `runs/ccl4r-7b-azure/w9704` | exit code 0 |
| `runs/ccl4r-7b-azure/w9705` | exit code 0 |
| `runs/ccl4r-7b-azure/w9706` | exit code 0 |
| `runs/ccl4r-7b-azure/w9707` | exit code 0 |
| `runs/ccl5-main-72b-g4/w9702` | exit code 0 |
| `runs/ccl5-main-72b-g4/w9703` | exit code 0 |
| `runs/ccl6-dev-7b/w9792-offices` | exit code 0 |
| `runs/ccl6-dev-7b/w9792-releases` | exit code 0 |
| `runs/ccl6-main-7b/w9708` | exit code 0 |
| `runs/ccl6-main-7b/w9709` | exit code 0 |
| `runs/ccl6-main-7b/w9710` | exit code 0 |
| `runs/ccl6-main-7b/w9711` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v10` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v4` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v5` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v6` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v7` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v8` | exit code 0 |
| `runs/ccl7-dev-1.5b/w9792-v9` | exit code 0 |
| `runs/ccl7-dev-7b/w9792` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v10` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v2` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v3` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v4` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v5` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v6` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v7` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v8` | exit code 0 |
| `runs/ccl7-dev-7b/w9792-v9` | exit code 0 |
| `runs/clx1-20261025/w9790` | exit code ? |
| `runs/clx10-20261025/w9790` | exit code ? |
| `runs/clx11-20261025/w9791` | exit code ? |
| `runs/clx12-20261026/w9792` | exit code ? |
| `runs/clx13-20261026/w9792` | exit code ? |
| `runs/clx14-20261026/w9792` | exit code ? |
| `runs/clx14c-20261025/w9790` | exit code ? |
| `runs/clx16-72b-system3-trial-20261026/w9792` | exit code 0 |
| `runs/clx2-20261025/w9790` | exit code ? |
| `runs/clx3b-20261025/w9790` | exit code ? |
| `runs/clx4-20261025/w9790` | exit code ? |
| `runs/clx5-20261025/w9790` | exit code ? |
| `runs/clx6-20261025/w9790` | exit code ? |
| `runs/clx7r-20261025/w9790` | exit code ? |
| `runs/clx8r-20261025/w9791` | exit code ? |
| `runs/clx9-20261025/w9790` | exit code ? |
| `runs/demo-test/smoke-1.5b` | exit code 0 |
| `runs/dr1-dev/w9792-v6-delete` | exit code 0 |
| `runs/dr1-dev/w9792-v6-retrain` | exit code 0 |
| `runs/dr1-dev-1.5b/w9792-v6-delete` | exit code 0 |
| `runs/dr1-dev-1.5b/w9792-v6-retrain` | exit code 0 |
| `runs/nb1-main-7b/w9702-lr2e-5` | exit code 0 |
| `runs/nb1-main-7b/w9702-lr5e-6` | exit code 0 |
| `runs/nb1-main-7b/w9703-lr2e-5` | exit code 0 |
| `runs/nb1-main-7b/w9703-lr5e-6` | exit code 0 |
| `runs/rg1-main-7b/w9702` | exit code 0 |
| `runs/rg1-main-7b/w9703` | exit code 0 |
| `runs/rw1-dev-1.5b/w9790-adapter` | exit code 0 |
| `runs/rw1-dev-7b/w9790` | exit code 0 |
| `runs/su1-main-7b/w9712` | exit code 0 |
| `runs/su1-main-7b/w9713` | exit code 0 |
| `runs/tx1-dev/w9792-read7b` | exit code 0 |
| `runs/tx1-dev/w9792-read7b-r2` | exit code 0 |
| `runs/wb1-dev-1.5b/w9792` | exit code 0 |
| `runs/wb1-dev-1.5b/w9792-v6` | exit code 0 |
| `runs/wb1-dev-7b/w9792-v6-a100` | exit code 0 |
| `runs/x10-dev-7b/w9793-s4` | exit code 0 |
| `runs/x10-main-7b/w9725` | exit code 0 |
| `runs/xf1-dev-olmo/w9792-s2` | exit code 0 |
| `runs/xf1-main-olmo/w9702` | exit code 0 |
| `runs/xf1-main-olmo/w9703` | exit code 0 |
| `runs/xf2-dev-olmoe/w9792-s2` | exit code 0 |
| `runs/xf2-main-olmoe/w9703` | exit code 0 |
| `runs/xfm-dev/gemma-w9792-s2` | exit code 0 |
| `runs/xfm-dev/llama-w9792-s2` | exit code 0 |
| `runs/xfm-dev/phi-w9792-s2` | exit code 0 |
