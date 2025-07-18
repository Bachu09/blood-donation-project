from playwright.sync_api import Page
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_join_form(page: Page):
    page.goto(f"{BASE_URL}/join")
    page.fill('input[name="name"]', "Volunteer Test")
    page.fill('input[name="email"]', "volunteer@example.com")
    page.fill('input[name="city"]', "Delhi")
    page.click('button[type="submit"]')

    page.wait_for_selector("#thank-message")
    assert "Thank you joining us" in page.inner_text("#thank-message")
