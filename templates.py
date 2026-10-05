# templates.py

HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5G + GPON NMS 系統 Demo</title>
    <style>
        body {
            background-color: #0f172a;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            border-bottom: 1px solid #1e293b;
            background-color: rgba(30, 41, 59, 0.8);
            padding: 15px 20px;
            position: sticky;
            top: 0;
            z-index: 50;
        }
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .badge {
            font-size: 11px;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: bold;
            color: #ffffff;
            transition: background-color 0.3s ease;
        }
        .bg-success { background-color: #22c55e; }
        .bg-danger { background-color: #ef4444; }
        
        .data-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #2d3748;
            font-family: monospace;
            font-size: 14px;
        }
        .data-row:last-child {
            border-bottom: none;
        }
        .text-label { color: #94a3b8; }
        .chart-container {
            width: 100%;
            height: 250px;
            position: relative;
            background-color: #0f172a;
            border-radius: 8px;
            border: 1px solid #1e293b;
            margin-top: 10px;
        }
        svg {
            width: 100%;
            height: 100%;
        }
        .chart-line-gpon {
            fill: none;
            stroke: #00d2ff;
            stroke-width: 3;
            stroke-linecap: round;
            transition: all 0.3s ease;
        }
        .chart-line-dl {
            fill: none;
            stroke: #3b82f6;
            stroke-width: 3;
            stroke-linecap: round;
            transition: all 0.3s ease;
        }
        .chart-line-ul {
            fill: none;
            stroke: #f97316;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-dasharray: 4;
            transition: all 0.3s ease;
        }
        .grid-line {
            stroke: #1e293b;
            stroke-width: 1;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th {
            color: #94a3b8;
            padding: 10px;
            text-align: left;
            border-bottom: 2px solid #334155;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #2d3748;
        }
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <div>
                <h1 style="margin: 0; font-size: 20px; color: #22d3ee;">⚡ 5G + GPON 工業級 NMS 系統 Demo</h1>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #94a3b8;">網絡監控 / NMS 數據同步 / SqLite 歷史資料數據展示</p>
            </div>
            <div id="sync-status" style="font-size: 12px; color: #10b981; font-weight: bold;">
                🟢 系統本機即時同步中 (3s)
            </div>
        </div>
    </header>

    <main class="main-container">
        <!-- 上方數據卡片區塊 -->
        <div class="grid-2">
            <!-- GPON 光纖實時狀態 -->
            <div class="card">
                <div class="card-header">
                    <h2 style="margin: 0; font-size: 15px; color: #22d3ee;">🌐 GPON 光纖實時狀態</h2>
                </div>
                <div>
                    <div class="data-row"><span class="text-label">OLT 實時狀態:</span><span id="txt-onu-count">--</span></div>
                    <div class="data-row"><span class="text-label">真實接收光功率:</span><span id="txt-gpon-power">-- dBm</span></div>
                    <div class="data-row"><span class="text-label">真實網路頻寬:</span><span id="txt-gpon-loss">-- Mbps</span></div>
                </div>
            </div>

            <!-- 5G 網卡專網監控 -->
            <div class="card">
                <div class="card-header">
                    <h2 style="margin: 0; font-size: 15px; color: #3b82f6;">📶 5G 網卡專網監控</h2>
                </div>
                <div>
                    <div class="data-row"><span class="text-label">5G CPE 信號強度 (RSRP):</span><span id="txt-rsrp">-- dBm</span></div>
                    <div class="data-row"><span class="text-label">真實網絡延遲 (Ping):</span><span id="txt-ping">-- ms</span></div>
                    <div class="data-row"><span class="text-label">模擬網絡卡片利用率:</span><span id="txt-usage">-- %</span></div>
                </div>
            </div>
        </div>

        <!-- 中間原生 SVG 折線圖區塊 -->
        <div class="grid-2">
            <!-- 左圖：GPON 接收光功率變動趨勢 -->
            <div class="card">
                <h3 style="margin: 0; font-size: 14px; color: #cbd5e1; display: flex; justify-content: space-between; align-items: center;">
                    <span>📈 GPON 接收光功率變動趨勢</span>
                    <span id="gpon-status-badge" class="badge bg-success">OLT ONLINE</span>
                </h3>
                <div class="chart-container" style="display: flex; align-items: stretch;">
                    <!-- 左側 Y 軸標籤 -->
                    <div style="display: flex; flex-direction: column; justify-content: space-between; height: 250px; padding-right: 8px; color: #64748b; font-size: 11px; text-align: right; width: 40px; user-select: none; box-sizing: border-box; padding-top: 5px; padding-bottom: 5px;">
                        <div>-15.0</div>
                        <div>-17.5</div>
                        <div>-20.0</div>
                        <div>-22.5</div>
                        <div>-25.0</div>
                    </div>
                    <!-- SVG 畫布 -->
                    <svg id="svg-gpon" style="flex: 1; height: 250px; overflow: visible;">
                        <line x1="0" y1="62.5" x2="100%" y2="62.5" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <line x1="0" y1="125" x2="100%" y2="125" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <line x1="0" y1="187.5" x2="100%" y2="187.5" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <path id="path-gpon" class="chart-line-gpon" d=""/>
                    </svg>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 11px; margin-top: 5px;">歷史變動趨勢 (dBm)</div>
            </div>

            <!-- 右圖：5G 專網即時吞吐量 -->
            <div class="card">
                <h3 style="margin: 0; font-size: 14px; color: #cbd5e1; display: flex; justify-content: space-between; align-items: center;">
                    <span>📊 5G 專網即時吞吐量</span>
                    <span id="fiveg-status-badge" class="badge bg-success">gNodeB ONLINE</span>
                </h3>
                <div class="chart-container" style="display: flex; align-items: stretch;">
                    <!-- 左側 Y 軸標籤 (動態更新) -->
                    <div id="fiveg-y-axis" style="display: flex; flex-direction: column; justify-content: space-between; height: 250px; padding-right: 8px; color: #64748b; font-size: 11px; text-align: right; width: 40px; user-select: none; box-sizing: border-box; padding-top: 5px; padding-bottom: 5px;">
                        <div id="fiveg-y-max">15M</div>
                        <div id="fiveg-y-mid2">11M</div>
                        <div id="fiveg-y-mid1">4M</div>
                        <div id="fiveg-y-min">0M</div>
                    </div>
                    <!-- SVG 畫布 -->
                    <svg id="svg-fiveg" style="flex: 1; height: 250px; overflow: visible;">
                        <line x1="0" y1="62.5" x2="100%" y2="62.5" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <line x1="0" y1="125" x2="100%" y2="125" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <line x1="0" y1="187.5" x2="100%" y2="187.5" class="grid-line" stroke="#1e293b" stroke-dasharray="3,3"/>
                        <path id="path-dl" class="chart-line-dl" d=""/>
                        <path id="path-ul" class="chart-line-ul" d=""/>
                    </svg>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 11px; margin-top: 5px;">
                    <span style="color: #3b82f6; margin-right: 15px;">● 下載 (DL)</span>
                    <span style="color: #f97316;">-- 上傳 (UL)</span>
                </div>
            </div>
        </div>

        <!-- 下方 SQLite 歷史數據表格 -->
        <div class="card" style="margin-top: 20px;">
            <h3 style="margin: 0 0 15px 0; font-size: 15px; color: #94a3b8;">SQLite 歷史資料存儲紀錄 (最新 10 筆)</h3>
            <div style="overflow-x: auto;">
                <table id="history-table">
                    <thead>
                        <tr>
                            <th>時間記錄</th>
                            <th>GPON 光功率 (dBm)</th>
                            <th>5G 下載吞吐量 (Mbps)</th>
                            <th>5G 上傳吞吐量 (Mbps)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td colspan="4" style="text-align: center; color: #64748b;">資料載入中...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        // 1. 核心線條路徑計算邏輯
        function generateSVGPath(dataArray, minVal, maxVal, width, height) {
            if (!dataArray || dataArray.length < 2) return "";
            const padding = 5;
            const usableHeight = height - (padding * 2);
            const stepX = width / (dataArray.length - 1);
            const valRange = maxVal - minVal;

            return dataArray.map((val, index) => {
                const x = index * stepX;
                const ratio = valRange === 0 ? 0.5 : (val - minVal) / valRange;
                const y = height - padding - (ratio * usableHeight);
                return (index === 0 ? 'M' : 'L') + ' ' + x.toFixed(1) + ' ' + y.toFixed(1);
            }).join(" ");
        }

        // 2. 定時請求 NMS 後端資料
        function fetchNMSStatus() {
            fetch('/api/network-status')
                .then(response => response.json())
                .then(data => {
                    console.log("成功接收到 NMS 資料:", data);

                    // 更新上方卡片文字數據
                    if (data.gpon) {
                        document.getElementById('txt-onu-count').textContent = data.gpon.olt_status;
                        document.getElementById('txt-gpon-power').textContent = data.gpon.optical_power_dbm + " dBm";
                        document.getElementById('txt-gpon-loss').textContent = data.gpon.real_bandwidth_mbps + " Mbps";
                    }
                    if (data.five_g) {
                        document.getElementById('txt-rsrp').textContent = data.five_g.cpe_rsrp_dbm + " dBm";
                        document.getElementById('txt-ping').textContent = data.five_g.real_latency_ms + " ms";
                        document.getElementById('txt-usage').textContent = data.five_g.slice_utilization_pct + " %";
                    }

                    // 即時繪製折線圖與告警
                    if (data.charts && data.charts.times) {
                        const svgGponElement = document.getElementById('svg-gpon');
                        const svgWidth = svgGponElement ? svgGponElement.clientWidth : 500;
                        const svgHeight = 250;

                        // --- GPON 渲染與告警 ---
                        const gponData = data.charts.gpon_power;
                        const gponPath = generateSVGPath(gponData, -25, -15, svgWidth, svgHeight);
                        document.getElementById('path-gpon').setAttribute('d', gponPath);

                        if (gponData && gponData.length > 0) {
                            const latestGpon = gponData[gponData.length - 1];
                            const gponBadge = document.getElementById('gpon-status-badge');
                            if (latestGpon < -24.0) {
                                gponBadge.className = "badge bg-danger";
                                gponBadge.textContent = "GPON ERROR";
                            } else {
                                gponBadge.className = "badge bg-success";
                                gponBadge.textContent = "OLT ONLINE";
                            }
                        }

                        // --- 5G 渲染、動態 Y 軸與告警 ---
                        const dlData = data.charts.download;
                        const ulData = data.charts.upload;

                        const all5gData = [...dlData, ...ulData];
                        const min5g = Math.min(...all5gData, 0);   
                        const max5g = Math.ceil(Math.max(...all5gData, 15)); 
                        const range = max5g - min5g;

                        document.getElementById('fiveg-y-max').textContent = max5g + "M";
                        document.getElementById('fiveg-y-mid2').textContent = (max5g - range * 0.33).toFixed(0) + "M";
                        document.getElementById('fiveg-y-mid1').textContent = (max5g - range * 0.66).toFixed(0) + "M";
                        document.getElementById('fiveg-y-min').textContent = min5g + "M";

                        const dlPath = generateSVGPath(dlData, min5g, max5g, svgWidth, svgHeight);
                        const ulPath = generateSVGPath(ulData, min5g, max5g, svgWidth, svgHeight);
                        document.getElementById('path-dl').setAttribute('d', dlPath);
                        document.getElementById('path-ul').setAttribute('d', ulPath);

                        if (dlData && dlData.length > 0) {
                            const latestDl = dlData[dlData.length - 1];
                            const fivegBadge = document.getElementById('fiveg-status-badge');
                            if (latestDl < 50) {
                                fivegBadge.className = "badge bg-danger";
                                fivegBadge.textContent = "5G LOW SPEED";
                            } else {
                                bluegBadge = document.getElementById('fiveg-status-badge');
                                fivegBadge.className = "badge bg-success";
                                fivegBadge.textContent = "gNodeB ONLINE";
                            }
                        }
                    }

                    // 3. 更新下方的 SQLite 歷史表格
                    if (data.history && data.history.length > 0) {
                        const tbody = document.querySelector('#history-table tbody');
                        if (tbody) {
                            let tableRows = [];
                            data.history.forEach(row => {
                                // A. 先抓取時間
                                const timeVal = row.timestamp || row.time || row.date || '--';
                                
                                // B. 自動分析物件裡面的所有數值
                                let detectedGpon = null;
                                let remainingNumbers = [];

                                for (let key in row) {
                                    if (key !== 'timestamp' && key !== 'time' && key !== 'date' && typeof row[key] === 'number') {
                                        let val = row[key];
                                        if (val < 0) {
                                            detectedGpon = val; // 負數一定是光功率 (dBm)
                                        } else {
                                            remainingNumbers.push(val); // 正數是吞吐量 (Mbps)
                                        }
                                    }
                                }

                                // C. 分配下載與上傳 (通常下載數據大於上傳數據)
                                remainingNumbers.sort((a, b) => b - a); // 由大到小排序
                                const dlVal = remainingNumbers[0] !== undefined ? remainingNumbers[0] : '--';
                                const ulVal = remainingNumbers[1] !== undefined ? remainingNumbers[1] : '--';
                                const gponVal = detectedGpon !== null ? detectedGpon : '--';

                                tableRows.push(
                                    '<tr>' +
                                        '<td>' + timeVal + '</td>' +
                                        '<td style="color: #00d2ff; font-weight:bold;">' + gponVal + ' dBm</td>' +
                                        '<td style="color: #3b82f6;">' + dlVal + ' Mbps</td>' +
                                        '<td style="color: #f97316; font-style: italic;">' + ulVal + ' Mbps</td>' +
                                    '</tr>'
                                );
                            });
                            tbody.innerHTML = tableRows.join('');
                        }
                    }
                })
                .catch(err => console.error("NMS 獲取資料發生錯誤:", err));
        }

        // 4. 初始化監聽與計時器啟動
        document.addEventListener('DOMContentLoaded', () => {
            fetchNMSStatus();
            setInterval(fetchNMSStatus, 3000);
        });
    </script>
</body>
</html>"""
