# SauceDemo UI 自动化测试项目（Playwright + pytest）

针对 [SauceDemo](https://www.saucedemo.com) 电商演示站做的 Web UI 自动化测试项目：用 Playwright 驱动真实浏览器，pytest 组织用例，页面对象模式（POM）管理元素与操作，覆盖登录、商品列表、购物车、结算四条主链路。

- 用例规模：15 条，分 4 个测试文件
- 执行结果：**15 passed，耗时 63.66 秒**（2026-10-04，Chrome + Chromium 内核）
- 技术栈：Python 3.14 / Playwright 1.63.0 / pytest 9.1.1 / pytest-playwright 0.9.0 / pytest-html 4.2.0
- 报告：`reports/pytest_report.html`

## 覆盖范围

| 模块 | 用例数 | 覆盖点 |
| --- | --- | --- |
| 登录 `test_login.py` | 6 | 标准用户登录成功、锁定用户被拒、密码错误提示、用户名为空、密码为空、退出登录 |
| 商品列表 `test_inventory.py` | 3 | 商品数量与价格条数、按价格升序排序、按名称降序排序 |
| 购物车 `test_cart.py` | 4 | 加购后徽标计数、加两件减一件、购物车页内容、购物车页移除后徽标清零 |
| 结算 `test_checkout.py` | 2 | 完整下单链路（加购 → 购物车 → 填写信息 → 提交 → 完成）、必填项校验（缺邮编） |

## 目录结构

```
Web_UI自动化测试/
├─ conftest.py                公共 fixture、页面对象注入、失败自动截图
├─ pytest.ini                 marker、浏览器参数、trace / 截图策略
├─ requirements.txt
├─ data/
│  └─ users.json              测试账号数据（与代码分离）
├─ pages/                     页面对象（POM）
│  ├─ base_page.py            基类：URL 拼接、等待、断言封装
│  ├─ login_page.py
│  ├─ inventory_page.py
│  ├─ cart_page.py
│  └─ checkout_page.py
├─ tests/
│  ├─ test_login.py
│  ├─ test_inventory.py
│  ├─ test_cart.py
│  └─ test_checkout.py
└─ reports/
   ├─ pytest_report.html      pytest-html 自包含报告
   ├─ screenshots/            失败用例自动截图（本目录不进仓库）
   └─ artifacts/              trace / 视频等 Playwright 产物（不进仓库）
```

## 设计要点

- **页面对象模式**：元素定位与操作封装在 `pages/`，用例只描述业务步骤，元素变更时只改一处。
- **fixture 复用**：`logged_in_inventory` 把「标准用户登录并停在商品列表页」抽成 fixture，购物车与结算用例直接复用，避免每个用例重复登录步骤。
- **数据与代码分离**：账号、地址等测试数据放在 `data/users.json`。
- **失败可诊断**：`--screenshot only-on-failure` + `--tracing retain-on-failure` 保留现场，另外 `conftest.py` 的 `pytest_runtest_makereport` 钩子会在用例失败时自动整页截图，并把截图路径写进 HTML 报告。
- **marker 分组**：`smoke`（冒烟）/ `regression`（回归）/ `ui`，支持 `pytest -m smoke` 只跑冒烟集。
- **不下载浏览器**：通过 `--browser-channel chrome` 直接使用本机已安装的 Chrome，省掉 `playwright install` 的几百 MB 下载。

## 运行方式

```powershell
cd "E:\软件测试\项目\Web_UI自动化测试"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 全量执行并生成 HTML 报告
.\.venv\Scripts\python.exe -m pytest --html=reports/pytest_report.html --self-contained-html

# 只跑冒烟用例
.\.venv\Scripts\python.exe -m pytest -m smoke

# 需要看到浏览器界面时
.\.venv\Scripts\python.exe -m pytest --headed
```

如果本机没有 Chrome，把 `pytest.ini` 里的 `--browser-channel chrome` 去掉，并执行一次 `.\.venv\Scripts\playwright.exe install chromium`。

## 执行结果（2026-10-04）

```
tests/test_cart.py::test_add_single_item_updates_badge[chromium] PASSED
tests/test_cart.py::test_add_two_items_and_remove_one[chromium] PASSED
tests/test_cart.py::test_cart_page_lists_added_item[chromium] PASSED
tests/test_cart.py::test_remove_item_from_cart_page_clears_badge[chromium] PASSED
tests/test_checkout.py::test_end_to_end_checkout_success[chromium] PASSED
tests/test_checkout.py::test_checkout_requires_postal_code[chromium] PASSED
tests/test_inventory.py::test_inventory_shows_six_items[chromium] PASSED
tests/test_inventory.py::test_sort_by_price_low_to_high[chromium] PASSED
tests/test_inventory.py::test_sort_by_name_descending[chromium] PASSED
tests/test_login.py::test_standard_user_can_login[chromium] PASSED
tests/test_login.py::test_locked_out_user_is_rejected[chromium] PASSED
tests/test_login.py::test_wrong_password_shows_credential_error[chromium] PASSED
tests/test_login.py::test_empty_username_shows_required_error[chromium] PASSED
tests/test_login.py::test_empty_password_shows_required_error[chromium] PASSED
tests/test_login.py::test_logout_returns_to_login_page[chromium] PASSED

15 passed in 63.66s
```

## 已知限制与下一步

- 被测对象是公网演示站，需要联网；本站数据固定（6 件商品），因此断言可以写死，换成真实业务系统后应改为数据驱动。
- 目前覆盖的是功能主链路，尚未覆盖异常网络、并发、多浏览器（Firefox / WebKit）兼容性。
- 下一步：接入 GitHub Actions，提交即跑 `-m smoke` 并归档 HTML 报告；补充失败重试与用例执行时长统计。
