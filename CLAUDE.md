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
