import streamlit as st
from datetime import datetime
from openai import OpenAI


# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Quán Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)


# ============================================================
# HIỂN THỊ ẢNH
# ============================================================

try:
    st.image(
        "4b48768552747ad1d57982cce438db69.jpg",
        use_container_width=True
    )
except:
    pass


# ============================================================
# DỮ LIỆU MENU
# ============================================================

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


# ============================================================
# DỮ LIỆU TOPPING
# ============================================================

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
    "Trân châu hoàng kim": 7000
}


# ============================================================
# GIÁ SIZE
# ============================================================

SIZE_PRICE = {
    "M": 0,
    "L": 5000
}


# ============================================================
# DỮ LIỆU CALO THAM KHẢO
# ============================================================

CALORIES = {
    "Trà sữa truyền thống": 300,
    "Trà sữa trân châu đường đen": 420,
    "Trà sữa matcha": 280,
    "Trà sữa socola": 380,
    "Trà sữa khoai môn": 360,
    "Trà sữa dâu": 300,
    "Trà sữa ô long": 260,
    "Trà đào": 180,
    "Trà vải": 190,
    "Trà chanh": 120
}


# ============================================================
# TOPPING PHÙ HỢP
# ============================================================

SUITABLE_TOPPINGS = {

    "Trà sữa truyền thống": [
        "Trân châu đen",
        "Trân châu trắng",
        "Pudding trứng"
    ],

    "Trà sữa trân châu đường đen": [
        "Trân châu đen",
        "Trân châu hoàng kim",
        "Kem cheese"
    ],

    "Trà sữa matcha": [
        "Trân châu trắng",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa socola": [
        "Trân châu đen",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa khoai môn": [
        "Trân châu trắng",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa dâu": [
        "Trân châu trắng",
        "Thạch trái cây",
        "Pudding trứng"
    ],

    "Trà sữa ô long": [
        "Trân châu đen",
        "Trân châu trắng",
        "Thạch dừa"
    ],

    "Trà đào": [
        "Thạch trái cây",
        "Thạch dừa",
        "Trân châu trắng"
    ],

    "Trà vải": [
        "Thạch trái cây",
        "Thạch dừa",
        "Trân châu trắng"
    ],

    "Trà chanh": [
        "Thạch trái cây",
        "Thạch dừa"
    ]
}


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("📋 Hệ thống tính hóa đơn")

st.divider()


# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name

st.divider()


# ============================================================
# CHỌN MÓN
# ============================================================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)


# ============================================================
# CỘT 1
# ============================================================

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


# ============================================================
# CỘT 2
# ============================================================

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


# ============================================================
# TÍNH GIÁ
# ============================================================

drink_price = MENU[drink]

size_price = SIZE_PRICE[size]

topping_price = sum(
    TOPPINGS[topping]
    for topping in toppings
)

unit_price = (
    drink_price
    + size_price
    + topping_price
)

total_item = unit_price * quantity


# ============================================================
# HIỂN THỊ GIÁ
# ============================================================

st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ/ly**  |  "
    f"Thành tiền: **{total_item:,} VNĐ**"
)


# ============================================================
# THÊM MÓN
# ============================================================

if st.button(
    "➕ Thêm món vào hóa đơn",
    use_container_width=True
):

    if not customer_name.strip():

        st.warning(
            "⚠️ Vui lòng nhập tên khách hàng trước."
        )

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
            f"✅ Đã thêm {quantity} ly "
            f"{drink} size {size} vào hóa đơn!"
        )


st.divider()


# ============================================================
# GIỎ HÀNG
# ============================================================

st.header("🛒 Danh sách món đã chọn")


if len(st.session_state.cart) == 0:

    st.info(
        "Chưa có món nào trong hóa đơn."
    )

else:

    grand_total = 0

    for i, item in enumerate(
        st.session_state.cart
    ):

        grand_total += item["total"]

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )


            # ------------------------------------------------
            # THÔNG TIN MÓN
            # ------------------------------------------------

            with col1:

                st.markdown(
                    f"### 🧋 {i + 1}. "
                    f"{item['drink']}"
                )

                topping_text = (
                    ", ".join(item["toppings"])
                    if item["toppings"]
                    else "Không có topping"
                )

                st.write(
                    f"**Size:** {item['size']} | "
                    f"**Đường:** {item['sugar']} | "
                    f"**Đá:** {item['ice']}"
                )

                st.write(
                    f"**Topping:** {topping_text}"
                )


            # ------------------------------------------------
            # GIÁ
            # ------------------------------------------------

            with col2:

                st.write(
                    f"**Số lượng:** "
                    f"{item['quantity']} ly"
                )

                st.write(
                    f"**Đơn giá:** "
                    f"{item['unit_price']:,} VNĐ"
                )

                st.write(
                   
