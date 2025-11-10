# ติดตั้งเครื่องมือ (local)
python -m pip install --upgrade pip
python -m pip install semgrep bandit pip-audit
# ถ้าใช้ Node:
cd apps/frontend
npm ci

# รันสแกนแบบรวม
cd <repo-root>
chmod +x scripts/run_full_scan.sh
./scripts/run_full_scan.sh

# ผลลัพธ์จะอยู่ใน ./ci-results
ls -la ./ci-results
# ตัวอย่าง: ดูสรุปจำนวน findings (ใช้ jq)
jq '.results | length' ./ci-results/semgrep.json || true
jq '.results | length' ./ci-results/bandit.json || true
jq '.vulnerabilities | length' ./ci-results/npm_audit.json || true
jq '.vulns | length' ./ci-results/pip_audit.json || true
