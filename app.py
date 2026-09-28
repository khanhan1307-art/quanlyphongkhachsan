# DỮ LIỆU PHÒNG MẪU
    # -----------------------------------------------------

    count = cur.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    if count == 0:

        rooms = []

        for floor in range(1, 4):

            for number in range(1, 7):

                room_number = f"{floor}{number:02d}"

                if number <= 2:
                    room_type = "Standard"
                    price = 650000

                elif number <= 4:
                    room_type = "Deluxe"
                    price = 850000

                elif number == 5:
                    room_type = "Suite"
                    price = 1200000

                else:
                    room_type = "Villa"
                    price = 1800000

                rooms.append(
                    (
                        room_number,
                        room_type,
                        price,
                        floor,
                        "Trống"
                    )
                )

        cur.executemany("""
            INSERT INTO rooms
            (room_number, room_type, price, floor, status)
            VALUES (?, ?, ?, ?, ?)
        """, rooms)

    # -----------------------------------------------------
    # DỊCH VỤ MẪU
    # -----------------------------------------------------

    count = cur.execute(
        "SELECT COUNT(*) FROM services"
    ).fetchone()[0]

    if count == 0:

        services = [
            ("Bữa sáng", 120000),
            ("Nước suối", 20000),
            ("Giặt ủi", 80000),
            ("Thuê xe máy", 150000),
            ("Taxi", 350000),
            ("Spa", 400000)
        ]

        cur.executemany("""
            INSERT INTO services
            (name, price)
            VALUES (?, ?)
        """, services)

    conn.commit()
    conn.close()


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def money(value):

    return f"{value:,.0f} ₫"


def calculate_nights(check_in, check_out):

    start = datetime.strptime(
        check_in, "%Y-%m-%d"
    ).date()

    end = datetime.strptime(
        check_out, "%Y-%m-%d"
    ).date()

    return max((end - start).days, 1)


def update_room_status():

    # Đưa phòng không còn khách về trống
    execute("""
        UPDATE rooms
        SET status = 'Trống'
        WHERE id NOT IN (
            SELECT room_id
            FROM bookings
            WHERE status = 'Đang ở'
        )
        AND status != 'Bảo trì'
    """)

    # Phòng đang ở
    execute("""
        UPDATE rooms
        SET status = 'Đang ở'
        WHERE id IN (
            SELECT room_id
            FROM bookings
            WHERE status = 'Đang ở'
        )
    """)

    # Phòng đã đặt
    execute("""
        UPDATE rooms
        SET status = 'Đã đặt'
        WHERE id IN (
            SELECT room_id
