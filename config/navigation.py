from dataclasses import dataclass


@dataclass(frozen=True)
class NavItem:
    id: str
    label: str
    href: str


PRIMARY_NAVIGATION = (
    NavItem("services", "Services", "/services/"),
    NavItem("work", "Work", "/work/"),
    NavItem("pricing", "Pricing", "/pricing/"),
    NavItem("process", "Process", "/process/"),
    NavItem("about", "About", "/about/"),
)

PRIMARY_CTA = NavItem(
    "start_project",
    "Start a Project",
    "/start/",
)
