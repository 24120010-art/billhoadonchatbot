import streamlit as st
from datetime import datetime
st.image("4b48768552747ad1d57982cce438db69.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)

# ==============================
# DỮ LIỆU MENU
# ==============================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 32000,
    "Trà sữa ô long": 33000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
    "Trân châu hoàng kim": 7000
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000
}

# ==============================
# KHỞI TẠO SESSION
# ==============================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ==============================
# TIÊU ĐỀ
# ==============================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("📋 Hệ thống tính hóa đơn")

st.divider()

# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name

st.divider()

# ==============================
# CHỌN MÓN
# ==============================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / thức uống",
        list(MENU.keys())
    )

    size = st.radio(
        "Size ly",
        ["M", "L"],
        horizontal=True
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        [
            "100% đường",
            "70% đường",
            "50% đường",
            "30% đường",
            "0% đường"
        ]
    )

    ice = st.selectbox(
        "Mức độ đá",
        [
            "100% đá",
            "70% đá",
            "50% đá",
            "30% đá",
            "Không đá"
        ]
    )

    toppings = st.multiselect(
        "Thêm topping",
        list(TOPPINGS.keys())
    )

# ==============================
# TÍNH TIỀN MÓN
# ==============================

drink_price = MENU[drink]
size_price = SIZE_PRICE[size]
topping_price = sum(TOPPINGS[t] for t in toppings)

unit_price = drink_price + size_price + topping_price
total_item = unit_price * quantity

st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ/ly**  |  "
    f"Thành tiền: **{total_item:,} VNĐ**"
)

# ==============================
# NÚT THÊM MÓN
# ==============================

if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    if not customer_name.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước.")
    else:

        item = {
            "drink": drink,
            "size": size,
            "sugar": sugar,
            "ice": ice,
            "toppings": toppings.copy(),
            "quantity": quantity,
            "unit_price": unit_price,
            "total": total_item
        }

        st.session_state.cart.append(item)

        st.success(
            f"✅ Đã thêm {quantity} ly {drink} size {size} vào hóa đơn!"
        )

st.divider()

# ==============================
# HIỂN THỊ GIỎ HÀNG
# ==============================

st.header("🛒 Danh sách món đã chọn")

if len(st.session_state.cart) == 0:

    st.info("Chưa có món nào trong hóa đơn.")

else:

    grand_total = 0

    for i, item in enumerate(st.session_state.cart):

        grand_total += item["total"]

        with st.container(border=True):

            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:
                st.markdown(
                    f"### 🧋 {i + 1}. {item['drink']}"
                )

                topping_text = (
                    ", ".join(item["toppings"])
                    if item["toppings"]
                    else "Không có topping"
                )

                st.write(
                    f"**Size:** {item['size']}  |  "
                    f"**Đường:** {item['sugar']}  |  "
                    f"**Đá:** {item['ice']}"
                )

                st.write(
                    f"**Topping:** {topping_text}"
                )

            with col2:
                st.write(
                    f"**Số lượng:** {item['quantity']} ly"
                )

                st.write(
                    f"**Đơn giá:** {item['unit_price']:,} VNĐ"
                )

                st.write(
                    f"**Thành tiền:** {item['total']:,} VNĐ"
                )

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{i}"
                ):
                    st.session_state.cart.pop(i)
                    st.rerun()

    st.divider()

    st.markdown(
        f"""
        <div style="
            background-color:#fff3cd;
            padding:20px;
            border-radius:10px;
            text-align:right;
        ">
            <h2>TỔNG THANH TOÁN</h2>
            <h1 style="color:#d63384;">
                {grand_total:,} VNĐ
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ==============================
    # THANH TOÁN
    # ==============================

    if st.button(
        "💳 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():
            st.warning("⚠️ Vui lòng nhập tên khách hàng.")
        else:
            st.session_state.paid = True
            st.rerun()


# ==============================
# HÓA ĐƠN SAU KHI THANH TOÁN
# ==============================

if st.session_state.paid:

    st.divider()

    st.success("🎉 Thanh toán thành công!")

    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    invoice_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    st.markdown(
        f"""
        <div style="
            border:2px solid #333;
            padding:25px;
            border-radius:12px;
            background-color:white;
        ">

        <div style="text-align:center;">
            <h1>🧋 QUÁN TRÀ SỮA</h1>
            <p>HÓA ĐƠN THANH TOÁN</p>
        </div>

        <hr>

        <p><b>Khách hàng:</b> {customer_name}</p>
        <p><b>Thời gian:</b> {invoice_time}</p>

        <hr>

        """,
        unsafe_allow_html=True
    )

    invoice_total = 0

    for i, item in enumerate(st.session_state.cart):

        invoice_total += item["total"]

        topping_text = (
            ", ".join(item["toppings"])
            if item["toppings"]
            else "Không có"
        )

        st.markdown(
            f"""
            <div style="
                padding:10px;
                border-bottom:1px solid #ddd;
            ">

            <b>{i + 1}. {item['drink']}</b><br>

            Size: {item['size']} |
            Số lượng: {item['quantity']} ly<br>

            Đường: {item['sugar']} |
            Đá: {item['ice']}<br>

            Topping: {topping_text}<br>

            Đơn giá: {item['unit_price']:,} VNĐ<br>

            <b>Thành tiền: {item['total']:,} VNĐ</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <hr>

        <div style="text-align:right;">
            <h2>TỔNG CỘNG</h2>
            <h1 style="color:#d63384;">
                {invoice_total:,} VNĐ
            </h1>
        </div>

        <hr>

        <div style="text-align:center;">
            <h3>💗 Cảm ơn quý khách đã sử dụng dịch vụ!</h3>
            <p>Hẹn gặp lại quý khách 🧋</p>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ==============================
    # ĐƠN MỚI
    # ==============================

    if st.button(
        "🔄 TẠO ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.customer_name = ""

        st.rerun()
