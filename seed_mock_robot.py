from app.database_models import Robot, get_session, create_db_and_tables

def seed_mock_robot():
    create_db_and_tables()

    robot = Robot(
        id="lekiwi-test",
        name="LeKiwi Test Unit",
        ros_domain=42,
        agent_host="main-control",
        components=["slam", "nav2"],
        # Manually convert Host objects to dicts
        hosts=[
            {"name": "main-control", "type": "x86", "portainer_endpoint_id": 1},
            {"name": "perception", "type": "orin", "portainer_endpoint_id": 2}
        ],
        watch_topics=["/scan", "/cmd_vel"]
    )

    with get_session() as session:
        if not session.get(Robot, robot.id):
            session.add(robot)
            session.commit()
            print(f"✅ Seeded robot: {robot.id}")
        else:
            print(f"ℹ️ Robot {robot.id} already exists")

if __name__ == "__main__":
    seed_mock_robot()
