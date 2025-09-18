import calendar
import datetime
import svgwrite


def weeks_in_year(year: int) -> int:
    """Return the number of ISO weeks in a given year (52 or 53)."""
    # ISO calendar: last week is the week containing Dec 28
    return datetime.date(year, 12, 28).isocalendar()[1]


def generate_heatmap_svg(year=2025, week_start=0, square_size=20,
                         stroke_width=1, stroke_color="black",
                         start_week=1, end_week=None,
                         output_file="heatmap.svg"):
    """
    Generate a vertical calendar heatmap in SVG.

    Args:
        year (int): Year to generate.
        week_start (int): First weekday (0=Monday, 6=Sunday).
        square_size (int): Size of each square cell.
        stroke_width (int/float): Stroke (border) thickness for day squares.
        stroke_color (str): Stroke color for day squares.
        start_week (int): First ISO week number to include.
        end_week (int|None): Last ISO week number to include (defaults to max for year).
        output_file (str): Filename for the SVG output.
    """

    max_weeks = weeks_in_year(year)
    if end_week is None or end_week > max_weeks:
        end_week = max_weeks

    if start_week < 1:
        start_week = 1
    if start_week > end_week:
        raise ValueError("start_week must be <= end_week")

    # Setup calendar
    cal = calendar.Calendar(firstweekday=week_start)

    # Create SVG drawing
    dwg = svgwrite.Drawing(output_file, profile='tiny')

    # Fonts
    font_size = square_size * 0.7
    font_family = "monospace"

    # Coordinates
    x_offset = 200  # space for week labels on the left

    # Track already labeled weeks
    labeled_weeks = set()

    # Loop through all weeks in the year
    for week in cal.yeardatescalendar(year, 1):
        for week_in_month in week:
            for days in week_in_month:
                for i, day in enumerate(days):
                    if day.year == year:
                        week_num = day.isocalendar()[1]

                        # Only include if in desired range
                        if not (start_week <= week_num <= end_week):
                            continue

                        # Row/col positions
                        row_y = (week_num - start_week) * square_size
                        col_x = i * square_size + x_offset

                        # Draw square
                        dwg.add(dwg.rect(
                            insert=(col_x, row_y),
                            size=(square_size, square_size),
                            fill="#cccccc",
                            stroke=stroke_color if stroke_width > 0 else "none",
                            stroke_width=stroke_width
                        ))

                        # Add week label once per row
                        if week_num not in labeled_weeks and i == 0:
                            week_start_date = day
                            week_end_date = day + datetime.timedelta(days=6)
                            label = f"W{week_num} {week_start_date:%b %d} - {week_end_date:%b %d}"

                            dwg.add(dwg.text(
                                label,
                                insert=(10, row_y + square_size * 0.8),
                                font_size=font_size,
                                font_family=font_family,
                                fill="black"
                            ))
                            labeled_weeks.add(week_num)

    # Save SVG
    dwg.save()
    print(f"SVG saved as {output_file} (weeks {start_week}–{end_week})")


if __name__ == "__main__":
    # Example usage
    generate_heatmap_svg(
        year=2025,
        week_start=0,       # Monday
        square_size=20,
        stroke_width=1,
        stroke_color="black",
        start_week=0,      # first week to include
        end_week=26,        # auto-clamped to max weeks in year
        output_file="output/heatmap.svg"
    )
