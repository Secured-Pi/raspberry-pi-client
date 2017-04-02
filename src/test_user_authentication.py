"""Test module for webcam_face_detector."""

from user_authentication import SERVER, PORT, send_img_to_server


def test_send_img_to_server():
    """Assert that an image can be sent to the server for verification."""
    t_rfid = 'testing-rfid'
    response = send_img_to_server('testing.gif', SERVER, PORT, t_rfid)
    assert hasattr(response, 'status_code')
