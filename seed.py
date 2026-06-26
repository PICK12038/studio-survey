import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from database import get_db, init_db
from auth import hash_password

SEED_CLASSES = [
    "高一(1)班", "高一(2)班", "高一(3)班",
    "高二(1)班", "高二(2)班", "高二(3)班",
    "高二(4)班", "高二(5)班",
    "高三集训(1)班", "高三集训(2)班", "高三集训(3)班",
    "高三集训(4)班", "高三集训(5)班", "高三集训(6)班", "高三集训(7)班",
]

SEED_TEACHERS = [
    # 高一(1)班
    ("张建国", 1, "素描静物,素描头像", 1),
    ("李明", 1, "色彩", 0),
    ("王芳", 1, "速写", 0),
    # 高一(2)班
    ("陈志强", 2, "素描静物,素描头像", 1),
    ("刘洋", 2, "色彩", 0),
    ("赵静", 2, "速写", 0),
    # 高一(3)班
    ("黄伟", 3, "素描静物,素描头像", 1),
    ("周敏", 3, "色彩", 0),
    ("吴磊", 3, "速写", 0),
    # 高二(1)班
    ("孙立", 4, "素描头像", 1),
    ("郑洁", 4, "色彩", 0),
    ("冯涛", 4, "速写", 0),
    # 高二(2)班
    ("朱峰", 5, "素描静物", 1),
    ("韩雪", 5, "色彩", 0),
    ("曹刚", 5, "速写", 0),
    # 高二(3)班
    ("许文", 6, "素描头像", 1),
    ("何丽", 6, "色彩", 0),
    ("吕强", 6, "速写", 0),
    # 高二(4)班
    ("施明", 7, "素描静物", 1),
    ("张玲", 7, "色彩", 0),
    ("沈兵", 7, "速写", 0),
    # 高二(5)班
    ("杨帆", 8, "素描头像", 1),
    ("姜丽", 8, "色彩", 0),
    ("潘勇", 8, "速写", 0),
    # 高三集训(1)班
    ("林志远", 9, "素描头像,色彩", 1),
    ("谢颖", 9, "速写", 0),
    ("唐军", 9, "素描静物", 0),
    # 高三集训(2)班
    ("罗辉", 10, "色彩,速写", 1),
    ("梁静", 10, "素描头像", 0),
    ("宋磊", 10, "素描静物", 0),
    # 高三集训(3)班
    ("彭博", 11, "素描头像", 1),
    ("董洁", 11, "色彩", 0),
    ("袁强", 11, "速写", 0),
    # 高三集训(4)班
    ("邓超", 12, "素描静物", 1),
    ("叶婷", 12, "色彩", 0),
    ("田亮", 12, "速写", 0),
    # 高三集训(5)班
    ("程浩", 13, "色彩", 1),
    ("郭静", 13, "素描头像", 0),
    ("钟伟", 13, "速写", 0),
    # 高三集训(6)班
    ("赖涛", 14, "速写,素描头像", 1),
    ("肖敏", 14, "色彩", 0),
    ("邱磊", 14, "素描静物", 0),
    # 高三集训(7)班
    ("廖峰", 15, "素描头像", 1),
    ("武洁", 15, "色彩", 0),
    ("龙强", 15, "速写", 0),
]


async def seed():
    await init_db()
    db = await get_db()

    # classes
    await db.execute("DELETE FROM classes")
    for i, name in enumerate(SEED_CLASSES):
        await db.execute("INSERT INTO classes (name, display_order) VALUES (?, ?)", (name, i + 1))

    # teachers
    await db.execute("DELETE FROM teachers")
    for name, class_id, subjects, is_head in SEED_TEACHERS:
        await db.execute(
            "INSERT INTO teachers (name, class_id, subjects, is_head_teacher) VALUES (?, ?, ?, ?)",
            (name, class_id, subjects, is_head),
        )

    # admin
    await db.execute("DELETE FROM admins")
    await db.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", ("admin", hash_password("admin123")))

    await db.commit()
    await db.close()
    print("Seed data inserted successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
