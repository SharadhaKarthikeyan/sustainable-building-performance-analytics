# Tableau Build Steps

This guide provides step-by-step instructions to build the **Sustainable Building Performance Analytics Dashboard** in Tableau Desktop.

---

## Step 1: Connect to Data
1. Open **Tableau Desktop**.
2. Under **Connect** > **To a File**, select **Text File**.
3. Select `dashboard/building_performance_dashboard_data.csv`.
4. Go to the **Sheet 1** tab.
5. In the **Data Pane**, check that the data types were correctly identified:
   - Numerical columns like `Floor Area Sqft` and `Site Eui` should be categorized as **Measures** (continuous #).
   - Category fields like `Building Type` and `Primary Material` should be **Dimensions** (ABC).
   - Flag variables like `Renewable Energy Flag` should be **Dimensions** (Boolean T/F).

---

## Step 2: Create Calculated Fields
Create the calculated fields needed for the dashboard (see `dashboard/calculated_fields.md` for exact formulas):
1. Right-click in the Data Pane and select **Create Calculated Field**.
2. Type the name and enter the Tableau calculation.
3. Repeat for:
   - `Total Buildings`
   - `Cost Overrun %`
   - `Delayed Project %`
   - `Operating Cost per Sqft`
   - `Renewable Adoption Rate`
   - `High Risk Building Count`
   - `Critical Risk Building Count`
   - `High or Critical Risk %`
   - `Weighted Payback Years`

---

## Step 3: Create Individual Sheets

### Sheet 1: Key KPI Cards
1. Create a sheet for each KPI.
2. Drag the measure (e.g. `Total Buildings`) onto **Text** on the Marks card.
3. Format the text (increase size to 20pt, bold).
4. Repeat this for all major KPIs.

### Sheet 2: Building Count by Type
1. Drag `Building Type` to **Rows**.
2. Drag `Total Buildings` (calculated count) to **Columns**.
3. Sort descending and color by `Building Type`.

### Sheet 3: EUI Distribution by Type (Box Plot)
1. Drag `Building Type` to **Columns**.
2. Drag `Energy Use Intensity Kbtu Sqft` to **Rows**.
3. Change Mark type to **Circle** and drag `Building Id` to **Detail** (to show individual building dots).
4. Go to the **Analytics** pane, drag **Box Plot** onto the cell area.

### Sheet 4: Risk Distribution Donut Chart
1. Create a Pie Chart: drag `Building Performance Risk Category` to **Color** and `Total Buildings` to **Angle**.
2. Double-click **Rows** and type `MIN(0.0)`. Repeat to create two identical axes.
3. Set Mark type to **Pie** for both.
4. On the second axis, remove all fields from Marks card, set color to White, and reduce size slightly.
5. Right-click the second axis and select **Dual Axis** to overlay.

### Sheet 5: EUI by Insulation Level
1. Drag `Insulation Level` to **Columns** (sort Low, Medium, High).
2. Drag `Energy Use Intensity Kbtu Sqft` to **Rows** (set to AVG).
3. Color by `Insulation Level`.

### Sheet 6: Contractor Cost Overrun %
1. Drag `Contractor Name` to **Rows**.
2. Drag `Cost Overrun %` to **Columns**.
3. Color by `Cost Overrun %` using a diverging red-green palette.

### Sheet 7: Retrofit Payback vs Savings
1. Drag `Payback Period Years` to **Columns**.
2. Drag `Estimated Annual Savings` to **Rows**.
3. Drag `Recommended Action` to **Color**.
4. Drag `Estimated Retrofit Cost` to **Size**.

---

## Step 4: Assemble the Dashboard
1. Click **New Dashboard**.
2. Set Size to **Generic Desktop (1366 x 768)** or **Automatic**.
3. Create a header block with the Title: **Sustainable Building Performance Analytics Dashboard**.
4. Drag a **Horizontal Container** for the Top KPI Row:
   - Drag Sheet 1 (KPI sheets) side-by-side into this container.
5. Create a 2x2 grid layout below the KPIs for the main charts by combining **Vertical** and **Horizontal Containers**.
6. Place Slicer filters on the right-hand column. Set filters to apply to **All Using This Data Source**.
7. Color Code consistently:
   - Set custom colors for `Building Performance Risk Category`: Low (Green), Medium (Yellow), High (Orange), Critical (Red).
