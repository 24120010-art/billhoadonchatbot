import streamlit as st
from datetime import datetime

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Quán Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)

# ============================================================
# ẢNH QUÁN
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


# ============================================================
# DỮ LIỆU CHO CHATBOT RULE-BASED
# ============================================================

# Calo tham khảo cho 1 ly size M, mức đường tiêu chuẩn.
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

# Topping phù hợp với từng loại thức uống.
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
# HÀM CHATBOT RULE-BASED
# ============================================================

def chatbot_reply(question):

    q = question.lower().strip()

    if not q:
        return "🤖 Em hãy nhập câu hỏi để anh có thể tư vấn nhé!"


    # --------------------------------------------------------
    # CHÀO HỎI
    # --------------------------------------------------------

    if any(word in q for word in [
        "xin chào",
        "chào",
        "hello",
        "hi"
    ]):
        return (
            "👋 Xin chào! Mình là chatbot của Quán Trà Sữa 🧋\n\n"
            "Bạn có thể hỏi mình:\n"
            "• Loại trà sữa nào giá cao nhất?\n"
            "• Món nào giá thấp nhất?\n"
            "• Trà sữa matcha kèm topping nào?\n"
            "• Loại nào ít ngọt?\n"
            "• Loại nào nhiều calo?"
        )


    # --------------------------------------------------------
    # GIÁ CAO NHẤT
    # --------------------------------------------------------

    if (
        ("cao nhất" in q or "đắt nhất" in q or "mắc nhất" in q)
        and ("giá" in q or "tiền" in q or "món" in q or "trà" in q)
    ):

        max_price = max(MENU.values())

        expensive = [
            name for name, price in MENU.items()
            if price == max_price
        ]

        result = "\n".join(
            [f"• {name}: {price:,} VNĐ" for name, price in MENU.items()
             if price == max_price]
        )

        return (
            f"💰 Các loại có giá cao nhất là:\n\n"
            f"{result}\n\n"
            f"Giá cao nhất: **{max_price:,} VNĐ/ly**."
        )


    # --------------------------------------------------------
    # GIÁ THẤP NHẤT
    # --------------------------------------------------------

    if (
        ("thấp nhất" in q
         or "rẻ nhất" in q
         or "giá thấp" in q
         or "rẻ" in q)
        and ("giá" in q
             or "món" in q
             or "trà" in q)
    ):

        min_price = min(MENU.values())

        cheap = [
            name for name, price in MENU.items()
            if price == min_price
        ]

        result = "\n".join(
            [f"• {name}: {price:,} VNĐ" for name, price in MENU.items()
             if price == min_price]
        )

        return (
            f"💵 Các món có giá thấp nhất là:\n\n"
            f"{result}\n\n"
            f"Giá thấp nhất: **{min_price:,} VNĐ/ly**."
        )


    # --------------------------------------------------------
    # TOPPING RẺ NHẤT
    # --------------------------------------------------------

    if (
        "topping" in q
        and (
            "rẻ nhất" in q
            or "thấp nhất" in q
            or "giá thấp" in q
        )
    ):

        min_topping = min(TOPPINGS.values())

        result = "\n".join(
            [
                f"• {name}: {price:,} VNĐ"
                for name, price in TOPPINGS.items()
                if price == min_topping
            ]
        )

        return (
            f"🍮 Topping có giá thấp nhất:\n\n"
            f"{result}\n\n"
            f"Giá từ **{min_topping:,} VNĐ**."
        )


    # --------------------------------------------------------
    # TOPPING ĐẮT NHẤT
    # --------------------------------------------------------

    if (
        "topping" in q
        and (
            "đắt nhất" in q
            or "mắc nhất" in q
            or "cao nhất" in q
        )
    ):

        max_topping = max(TOPPINGS.values())

        result = "\n".join(
            [
                f"• {name}: {price:,} VNĐ"
                for name, price in TOPPINGS.items()
                if price == max_topping
            ]
        )

        return (
            f"🍮 Topping có giá cao nhất:\n\n"
            f"{result}\n\n"
            f"Giá: **{max_topping:,} VNĐ**."
        )


    # --------------------------------------------------------
    # ÍT NGỌT
    # --------------------------------------------------------

    if (
        "ít ngọt" in q
        or "ít đường" in q
        or "không ngọt" in q
        or "0 đường" in q
    ):

        return (
            "🥤 Nếu bạn thích ít ngọt, có thể chọn:\n\n"
            "• Trà chanh – vị thanh, dễ uống\n"
            "• Trà đào – vị trái cây nhẹ\n"
            "• Trà vải – vị ngọt tự nhiên\n"
            "• Trà sữa ô long – có thể chọn 30% hoặc 0% đường\n"
            "• Trà sữa matcha – có thể chọn 30% hoặc 0% đường\n\n"
            "💡 Khi đặt món, bạn có thể chọn mức **30% hoặc 0% đường**."
        )


    # --------------------------------------------------------
    # NHIỀU CALO NHẤT
    # --------------------------------------------------------

    if (
        "nhiều calo" in q
        or "cao calo" in q
        or "calo cao" in q
        or "nhiều năng lượng" in q
    ):

        max_calories = max(CALORIES.values())

        result = "\n".join(
            [
                f"• {name}: khoảng {cal:,} kcal"
                for name, cal in CALORIES.items()
                if cal == max_calories
            ]
        )

        return (
            f"🔥 Loại có lượng calo tham khảo cao nhất:\n\n"
            f"{result}\n\n"
            f"Khoảng **{max_calories} kcal/ly size M** "
            f"ở mức đường tiêu chuẩn."
        )


    # --------------------------------------------------------
    # ÍT CALO NHẤT
    # --------------------------------------------------------

    if (
        "ít calo" in q
        or "calo thấp" in q
        or "ít năng lượng" in q
    ):

        min_calories = min(CALORIES.values())

        result = "\n".join(
            [
                f"• {name}: khoảng {cal:,} kcal"
                for name, cal in CALORIES.items()
                if cal == min_calories
            ]
        )

        return (
            f"🥤 Loại có lượng calo tham khảo thấp nhất:\n\n"
            f"{result}\n\n"
            f"Khoảng **{min_calories} kcal/ly size M** "
            f"ở mức đường tiêu chuẩn."
        )


    # --------------------------------------------------------
    # TÌM MÓN + TOPPING PHÙ HỢP
    # --------------------------------------------------------

    for drink_name in MENU.keys():

        keywords = drink_name.lower().split()

        if drink_name.lower() in q:

            topping_list = SUITABLE_TOPPINGS[drink_name]

            toppings_text = "\n".join(
                [f"• {topping}" for topping in topping_list]
            )

            return (
                f"🧋 **{drink_name}** có giá "
                f"**{MENU[drink_name]:,} VNĐ/ly size M**.\n\n"
                f"🍮 Một số topping phù hợp:\n"
                f"{toppings_text}\n\n"
                f"Bạn có thể chọn thêm topping khi đặt món."
            )


    # --------------------------------------------------------
    # HỎI GIÁ MỘT MÓN
    # --------------------------------------------------------

    if (
        "giá" in q
        or "bao nhiêu tiền" in q
        or "bao nhiêu" in q
    ):

        for drink_name, price in MENU.items():

            if drink_name.lower() in q:

                return (
                    f"🧋 **{drink_name}** có giá:\n\n"
                    f"• Size M: **{price:,} VNĐ**\n"
                    f"• Size L: **{price + SIZE_PRICE['L']:,} VNĐ**"
                )


    # --------------------------------------------------------
    # HỎI CALO MỘT MÓN
    # --------------------------------------------------------

    if "calo" in q or "kcal" in q:

        for drink_name, calories in CALORIES.items():

            if drink_name.lower() in q:

                return (
                    f"🧋 **{drink_name}** có khoảng "
                    f"**{calories} kcal/ly size M** "
                    f"ở mức đường tiêu chuẩn.\n\n"
                    f"⚠️ Lượng calo thực tế có thể thay đổi "
                    f"theo mức đường, size và topping."
                )


    # --------------------------------------------------------
    # HỎI TOPPING CHUNG
    # --------------------------------------------------------

    if "topping" in q:

        topping_text = "\n".join(
            [
                f"• {name}: {price:,} VNĐ"
                for name, price in TOPPINGS.items()
            ]
        )

        return (
            "🍮 Các loại topping hiện có:\n\n"
            f"{topping_text}"
        )


    # --------------------------------------------------------
    # HỎI MENU
    # --------------------------------------------------------

    if (
        "menu" in q
        or "thức uống" in q
        or "có những món gì" in q
        or "có món gì" in q
    ):

        menu_text = "\n".join(
            [
                f"• {name}: {price:,} VNĐ"
                for name, price in MENU.items()
            ]
        )

        return (
            "📋 **MENU QUÁN TRÀ SỮA**\n\n"
            f"{menu_text}"
        )


    # --------------------------------------------------------
    # CÂU HỎI KHÔNG NHẬN DIỆN ĐƯỢC
    # --------------------------------------------------------

    return (
        "🤖 Xin lỗi, mình chưa hiểu câu hỏi này.\n\n"
        "Bạn có thể thử hỏi:\n"
        "• Trà sữa nào giá cao nhất?\n"
        "• Món nào giá thấp nhất?\n"
        "• Trà sữa matcha kèm topping nào?\n"
        "• Loại nào ít ngọt?\n"
        "• Loại nào nhiều calo?\n"
        "• Trà sữa ô long giá bao nhiêu?\n"
        "• Topping nào rẻ nhất?\n"
        "• Menu có những món gì?"
    )


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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


# ============================================================
# TÍNH TIỀN MÓN
# ============================================================

drink_price = MENU[drink]
size_price = SIZE_PRICE[size]

topping_price = sum(
    TOPPINGS[t]
    for t in toppings
)

unit_price = (
    drink_price
    + size_price
    + topping_price
)

total_item = unit_price * quantity


st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ/ly**  |  "
    f"Thành tiền: **{total_item:,} VNĐ**"
)


# ============================================================
# NÚT THÊM MÓN
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
                    f"**Size:** {item['size']}  |  "
                    f"**Đường:** {item['sugar']}  |  "
                    f"**Đá:** {item['ice']}"
                )

                st.write(
                    f"**Topping:** {topping_text}"
                )

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
                    f"**Thành tiền:** "
                    f"{item['total']:,} VNĐ"
                )

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{i}"
                ):

                    st.session_state.cart.pop(i)

                    st.rerun()


    st.divider()


    # ========================================================
    # TỔNG THANH TOÁN
    # ========================================================

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


    # ========================================================
    # THANH TOÁN
    # ========================================================

    if st.button(
        "💳 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():

            st.warning(
                "⚠️ Vui lòng nhập tên khách hàng."
            )

        else:

            st.session_state.paid = True

            st.rerun()


# ============================================================
# HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================

if st.session_state.paid:

    st.divider()

    st.success(
        "🎉 Thanh toán thành công!"
    )

    st.header(
        "🧾 HÓA ĐƠN THANH TOÁN"
    )

    invoice_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


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

            <p>
                <b>Khách hàng:</b>
                {customer_name}
            </p>

            <p>
                <b>Thời gian:</b>
                {invoice_time}
            </p>

            <hr>
        """,
        unsafe_allow_html=True
    )


    invoice_total = 0


    for i, item in enumerate(
        st.session_state.cart
    ):

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

                <b>
                    {i + 1}. {item['drink']}
                </b>
                <br>

                Size: {item['size']} |
                Số lượng: {item['quantity']} ly
                <br>

                Đường: {item['sugar']} |
                Đá: {item['ice']}
                <br>

                Topping: {topping_text}
                <br>

                Đơn giá:
                {item['unit_price']:,} VNĐ
                <br>

                <b>
                    Thành tiền:
                    {item['total']:,} VNĐ
                </b>

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

                <h3>
                    💗 Cảm ơn quý khách
                    đã sử dụng dịch vụ!
                </h3>

                <p>
                    Hẹn gặp lại quý khách 🧋
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # ========================================================
    # ĐƠN MỚI
    # ========================================================

    if st.button(
        "🔄 TẠO ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.customer_name = ""
        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# CHATBOT TƯ VẤN
# ============================================================

st.divider()

st.header("🤖 Chatbot tư vấn trà sữa")

st.write(
    "Chatbot hoạt động dựa trên luật và dữ liệu menu của quán."
)


# ============================================================
# CÂU HỎI GỢI Ý
# ============================================================

st.markdown("**💡 Bạn có thể hỏi:**")

suggestion_cols = st.columns(5)

suggestions = [
    "Trà sữa nào giá cao nhất?",
    "Món nào giá thấp nhất?",
    "Trà sữa matcha kèm topping nào?",
    "Loại nào ít ngọt?",
    "Loại nào nhiều calo?"
]

for i, suggestion in enumerate(suggestions):

    with suggestion_cols[i]:

        if st.button(
            suggestion,
            key=f"suggestion_{i}",
            use_container_width=True
        ):

            answer = chatbot_reply(
                suggestion
            )

            st.session_state.chat_history.append(
                {
                    "user": suggestion,
                    "bot": answer
                }
            )


# ============================================================
# HIỂN THỊ LỊCH SỬ CHAT
# ============================================================

if st.session_state.chat_history:

    st.markdown("### 💬 Hội thoại")

    for chat in st.session_state.chat_history:

        st.markdown(
            f"""
            <div style="
                background-color:#f8f9fa;
                padding:12px;
                border-radius:10px;
                margin-bottom:8px;
            ">

                <b>👤 Bạn:</b>
                {chat["user"]}

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background-color:#fff3cd;
                padding:12px;
                border-radius:10px;
                margin-bottom:15px;
            ">

                <b>🤖 Chatbot:</b><br>

                {chat["bot"].replace(chr(10), "<br>")}

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# Ô NHẬP CHAT
# ============================================================

user_question = st.text_input(
    "💬 Nhập câu hỏi của bạn:",
    placeholder=(
        "Ví dụ: Trà sữa nào nhiều calo?"
    ),
    key="chat_input"
)


if st.button(
    "📨 Gửi câu hỏi",
    use_container_width=True
):

    if user_question.strip():

        answer = chatbot_reply(
            user_question
        )

        st.session_state.chat_history.append(
            {
                "user": user_question,
                "bot": answer
            }
        )

        st.rerun()

    else:

        st.warning(
            "⚠️ Vui lòng nhập câu hỏi."
                )
