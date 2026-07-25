# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

이 파일은 Claude Code가 본 저장소에서 작업할 때 참고하는 가이드입니다.

=======================================================================================

> **팀 프로젝트 주의사항** — 이 파일은 팀과 공유됩니다.
> 작업이 끝난 뒤 **`git push` 하기 전에 항상 이 CLAUDE.md를 최신 상태로 업데이트**해 주세요.
> (새 모듈 추가, CLI 인자 변경, 학습 파이프라인 수정 등 반영)

## 1. Git 커밋/푸쉬 규칙 (팀 합의)

> **❗ 매우 중요 — Claude Code 사용 시**
>
> - 커밋 메시지에 **`Co-Authored-By: Claude ...` 줄(co-author 트레일러)을 절대 포함하지 말 것.**
>   기본 동작에서 추가되는 `Co-Authored-By: Claude Opus ...` 같은 라인은 모두 **제거하고** 커밋한다.
> - 마찬가지로 `🤖 Generated with [Claude Code]` 같은 자동 서명 푸터도 넣지 않는다.
> - 즉, 커밋 메시지는 **사람이 직접 쓴 것처럼 본문(제목 + 설명)만** 남긴다.

### 커밋 예시 (OK)
```
feat(losses): CB-Focal 가중치 정규화 방식 변경

weight.sum() == num_classes 가 되도록 정규화하여
official impl 과 동치가 되게 수정.
```

### 커밋 예시 (NG — 이렇게 쓰지 말 것)
```
feat(losses): CB-Focal 가중치 정규화 방식 변경

...

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

### 푸쉬 전 체크리스트
1. 변경된 코드/명령/파이프라인을 **CLAUDE.md (이 파일) 와 README.md** 에 반영했는가?
2. 커밋 메시지에 `Co-Authored-By:` 또는 Claude 자동 서명이 들어가 있지 않은가?
3. `outputs/`, `data/`, `*.pth`, 큰 캐시 파일 등을 실수로 커밋하지 않았는가? (필요하면 `.gitignore` 확인)
4. (가능하면) 학습 한 epoch 라도 돌려서 import / dataloader / loss 가 깨지지 않는지 확인.

---

## Train/Test 분할 (`split.env` + `split_util.py`)

`Reformatted_*.csv` 를 `training-flow.csv` / `test-flow.csv` 로 나누는 공용 유틸.

- **정책은 전부 `split.env` 에 데이터셋별 한 줄로 하드코딩.** 비율/시드/보존여부를
  바꾸려면 이 파일 **한 곳만** 고치면 전체에 반영됨. `split_util.py` 는 이 설정을
  읽어 적용만 하는 얕은 러너 — 유틸에 비율/데이터셋명을 하드코딩하지 말 것.
- **값 문법** (우변):
  - `<ratio>,<seed>` — `attack_flag` 기준 stratified 분할 (pandas, 전체 메모리 로드).
  - `<ratio>,<seed>,lazy` — 동일 분할이지만 polars `scan_csv` 로 **클래스별로 하나씩만**
    메모리에 올림. 초대형 파일용 (`bot-iot`, `cicids2018-imp`, `lspr23`).
    출력이 클래스별 블록 정렬됨(블록 내 셔플) — 학습 시 셔플 전제.
  - `official` — 원본 배포본의 train/test 분할 보존 (`nsl-kdd`, `unsw-nb15`).
    `split` provenance 컬럼 기준으로 분리. 재분할 시 논문 재현성 깨지므로 보존.
  - `pipeline` — 자체 download.py 가 이미 두 파일 생성 (`cicids2017/2018`, `ciciot2023`,
    `ton-iot`, `mirai`). 러너가 건너뜀.
- **`official` 데이터셋 규칙**: 해당 download.py 는 concat 전에
  `df_train["split"]="train"`, `df_test["split"]="test"` 태그를 남기고, process() 는
  `split` 컬럼을 feature 에서 제외해 맨 끝에 보존해야 함. (예: `unsw-nb15/download.py`)
- **실행**: `python3 split_util.py <dataset> [...]`.
  `--keep`(중간 Reformatted 유지, 기본은 삭제), `--test-ratio` / `--seed` 로 일시 오버라이드.
- 새 데이터셋 추가 시 `split.env` 에 한 줄 등록할 것. `split.env`/`split_util.py` 는
  git 추적, 데이터 CSV 3종(Reformatted/training-flow/test-flow)은 `*.csv` 로 gitignore.

---

## 데이터셋 확장 작업 현황 (Phase 2)

> 마지막 업데이트: 2026-05-30

### 전체 완료 datasets (데이터 검증됨, unmapped=0)

| Dataset | 디렉토리 | 행 수 | Kill-chain steps | 소스 | 비고 |
|---|---|---|---|---|---|
| KDDCup 1999 | `kddcup1999/` | 494k | 0,1,4,5,7 | Kaggle `galaxyh/kdd-cup-1999-data` | — |
| CTU-13 | `ctu-13/` | 1.6M | 0,6 | Kaggle `dhoogla/ctu13` | 13개 parquet concat |
| N-BaIoT | `n-baiot/` | 2.4M+ | 0,1,7 | Kaggle `mkashifn/nbaiot-dataset` | 파일명 레이블 추출 |
| CIDDS-001 | `cidds-001/` | 204k | 0,1,4 | Kaggle `dhoogla/cidds001` | parquet |
| CIDDS-002 | `cidds-002/` | 2.6M | 0,1 | Kaggle `dhoogla/cidds002` | parquet |
| IoTID20 | `iotid20/` | 626k | 0,1,4,6,7 | Kaggle `rohulaminlabid/iotid20-dataset` | Cat 컬럼 |
| HIKARI-2021 | `hikari-2021/` | 555k | 0,1,4,7 | Kaggle `kk0105/allflowmeter-hikari2021` | traffic_category 컬럼 |
| NSL-KDD | `nsl-kdd/` | 148k | 0,1,4,5,6,7 | Kaggle `hassan06/nslkdd` | KDDTrain+.txt 파싱 |
| UNSW-NB15 | `unsw-nb15/` | 258k | 0,1,4,5,6,7 | Kaggle `mrwellsdavid/unsw-nb15` | 10개 attack_cat |
| InSDN | `insdn/` | 344k | 0,1,4,6,7 | Kaggle `badcodebuilder/insdn-dataset` | 3 CSV concat |
| CIC-DDoS2019 | `cic-ddos2019/` | 431k | 0,3,7 | Kaggle `dhoogla/cicddos2019` | 17개 parquet, 전체 재다운로드 |
| Bot-IoT | `bot-iot/` | 73.4M | 0,1,7 | Kaggle `vigneshvenkateswaran/bot-iot` | 75 CSV, process() 청크처리 |
| CIC-IDS2017 Imp. | `cicids2017-imp/` | 2.1M | 0,1,4,6,7 | distrinet URL (328MB) | Liu et al. 2022 |
| CSE-CIC-IDS2018 Imp. | `cicids2018-imp/` | 63.2M | 0,4,6,7 | distrinet URL (9.7GB) | Liu et al. 2022 |
| Kitsune | `kitsune/` | 1.8M | 0,1,4,6,7 | Kaggle `ymirsky/network-attack-dataset-kitsune` | 라이선스 불필요 |
| IoT-23 | `iot-23/` | 2.6M | 0,1,6,7 | 공식 CTU 사이트 | Zeek conn.log 파싱 |

### download.py 있음, 데이터 미취득 (Kaggle 라이선스 수락 필요)

| Dataset | 디렉토리 | Kaggle 소스 | 대안 |
|---|---|---|---|
| AWID2 | `awid2/` | `kolias93/awid2-wifi-intrusion-dataset` | `python3 download.py register NAME LAST EMAIL AFFIL` |
| AWID3 | `awid3/` | `chatzoglou/awid3` | `python3 download.py register NAME LAST EMAIL AFFIL` |

### download.py 있음, 데이터 미취득 (기타)

| Dataset | 디렉토리 | 이유 |
|---|---|---|
| Mirai Botnet Dataset | `mirai/` | download.py 없음 (pcap + label 파일 기반, 처리 방식 미정) |

### 코드 구조 (모든 download.py 공통 패턴)

```python
KAGGLE_DATASET = "author/dataset-name"
INPUT_FILENAME  = "DatasetName.csv"        # 원본 concat/중간파일
OUTPUT_FILENAME = "Reformatted_DatasetName.csv"  # 최종 표준 포맷

KILL_CHAIN = {"benign": 0, "scan": 1, "exploit": 4, "c&c": 6, "ddos": 7, ...}

def download():   # Kaggle/URL에서 다운로드 → INPUT_FILENAME 생성
def process():    # INPUT_FILENAME → OUTPUT_FILENAME (표준 3컬럼 추가)

# 표준 출력 포맷: feature_columns... | attack_name | attack_flag | attack_step
```

### 인용 / BibTeX (`citations/`)

- 각 데이터셋의 **원본논문 BibTeX** 는 `citations/<dataset>.bib` 에 있음 (파일명 = 디렉토리명, 현재 29개).
- README 연동:
  - `Available Datasets` 표 — 데이터셋 **이름 링크가 곧 `citations/*.bib`** (디렉토리 링크 아님).
  - `Dataset Details` — `Source` = 원본논문명 + `[[BibTeX]]` 링크, `File Source` = 실제 다운로드 소스(Kaggle/URL 등).
- **새 데이터셋 추가 시**: `citations/<dataset>.bib` 생성 + README 표의 이름 링크를 해당 `.bib` 로 연결 + Details 의 Source/File Source 도 같이 추가할 것.
- 저자/연도/venue/DOI 는 **DBLP 기준으로 검증**해서 기입.

### Kaggle 소스 403 현황 (2026-05-30 전수 검증)

| 상태 | Dataset (download.py 실제 ID) | 비고 |
|---|---|---|
| ❌ 403 | awid2: `kolias93/awid2-wifi-intrusion-dataset` | 공식 사이트 이메일 요청 가능 |
| ❌ 403 | awid3: `chatzoglou/awid3` | 동일 |
| ✅ 정상 | 나머지 모두 (17개) | — |

### 알려진 이슈

- **Bot-IoT**: `subcategory ` 컬럼 trailing space → `errors="ignore"`. 14GB CSV라 process() 500k 청크 방식.
- **CTU-13**: attack_name에 `flow=` prefix → `str.replace(r"^flow=", "")`.
- **CIC-DDoS2019**: Kaggle v3 소스에 `netbios/ldap/mssql/portmap/udp/webddos/udplag` 신규 레이블 추가됨 → KILL_CHAIN 확장 완료.
- **NSL-KDD**: KDDTest+.txt에 KDD'99에 없는 공격 타입 포함(saint/mscan/apache2 등) → KILL_CHAIN 확장 완료.
- **CIC-DDoS2019**: KILL_CHAIN에 `netbios`, `ldap`, `mssql`, `portmap`, `udp`, `webddos`, `udplag` 등 신규 레이블 → 확장 완료.
- **IoT-23**: 공식 CTU 사이트 스트리밍. Zeek conn.log 마지막 탭필드 `tunnel_parents  label  detailed-label` (공백구분). okiru/okiru-attack/c&c-heartbeat-filedownload KILL_CHAIN 추가 완료.
- **Kitsune**: `ymirsky/network-attack-dataset-kitsune` (라이선스 불필요). Mirai Botnet labels 파일 소문자(`mirai_labels.csv`) → 대소문자 무시 매칭. labels 형식 2종: 헤더+인덱스컬럼(`x`), 헤더없이 0/1 (Mirai).
- **CIC-IDS2017/2018 Imp.**: `- Attempted` suffix 레이블 → step 0 처리 (공격 의도지만 실제 악성 행동 없음).
- **n-baiot/nf-ton-iot-v3**: 캐시 손상 시 "Bad magic number" → `rm -rf ~/.cache/kagglehub/datasets/{id}` 후 재실행.
- **LSPR23**: Zenodo `ls23pr_flows.zip` 는 루트에 단일 CSV(`ls23pr_v1.csv`, ZIP64 >4GB)만 들어있음 → `INPUT_FILE=./ls23pr_v1.csv`, `OUTPUT_FILE=./Reformatted_LSPR23.csv` (기존 `LSPR23/ls23pr_flows/` 하드코딩 경로는 오류였음).
- **X-IIoTID**: 실제 라벨 컬럼은 `class1`(세부공격 19종)/`class2`(전술 10종)/`class3`(Attack/Normal). `class` 아님 → REQUIRED_COLUMNS·rename 을 `class1→attack_step`, `class2→attack_name`, `class3→attack_flag` 로 수정. KILL_CHAIN 키를 실제 class1 값(`scanning_vulnerability`, `tcp relay`, `crypto-ransomware` 등)에 맞춰 재작성해 unmapped=0 (820,834행 검증).
