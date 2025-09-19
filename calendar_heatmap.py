import calendar
import datetime
import svgwrite


def weeks_in_year(year: int) -> int:
    """Return the number of ISO weeks in a given year (52 or 53)."""
    return datetime.date(year, 12, 28).isocalendar()[1]


def generate_heatmap_svg(year=2025, week_start=0, square_size=20,
                         stroke_width=1, stroke_color="black",
                         start_week=1, end_week=None,
                         label_width=10.0, font_family="Roboto Bold",
                         cell_fill="#cccccc", label_fill="#eeeeee",
                         row_line=False, row_line_margin_squares=0.25, row_line_length_squares=1.0,
                         output_file="heatmap.svg"):
    """
    Generate a vertical calendar heatmap in SVG with a separate header row.
    """

    max_weeks = weeks_in_year(year)
    if end_week is None or end_week > max_weeks:
        end_week = max_weeks

    if start_week < 1:
        start_week = 1
    if start_week > end_week:
        raise ValueError("start_week must be <= end_week")

    cal = calendar.Calendar(firstweekday=week_start)
    dwg = svgwrite.Drawing(output_file, profile='tiny')

    font_size = square_size * 0.5
    label_cell_width = label_width * square_size

    labeled_weeks = set()

    # --- Weekday header squares ---
    weekdays = list(calendar.day_abbr)
    weekdays = weekdays[week_start:] + weekdays[:week_start]
    header_row_y = 0
    for i, wd in enumerate(weekdays):
        col_x = i * square_size + label_cell_width
        # Draw header square
        dwg.add(dwg.rect(
            insert=(col_x, header_row_y),
            size=(square_size, square_size),
            fill=label_fill,
            stroke=stroke_color if stroke_width > 0 else "none",
            stroke_width=stroke_width
        ))
        # Draw header text
        dwg.add(dwg.text(
            wd[0],
            insert=(col_x + square_size / 2, header_row_y + square_size / 2 + font_size / 3),
            font_size=font_size,
            font_family=font_family,
            text_anchor="middle",
            fill="black"
        ))

    # --- Calendar weeks ---
    for week in cal.yeardatescalendar(year, 1):
        for week_in_month in week:
            for days in week_in_month:
                for i, day in enumerate(days):
                    if day.year == year:
                        week_num = day.isocalendar()[1]
                        if not (start_week <= week_num <= end_week):
                            continue

                        # Row position (+1 for header row)
                        row_y = (week_num - start_week + 1) * square_size
                        col_x = i * square_size + label_cell_width

                        # Draw label cell only for the first day in the week
                        if week_num not in labeled_weeks and i == 0:
                            week_start_date = day
                            week_end_date = day + datetime.timedelta(days=6)

                            dwg.add(dwg.rect(
                                insert=(0, row_y),
                                size=(label_cell_width, square_size),
                                fill=label_fill,
                                stroke=stroke_color if stroke_width > 0 else "none",
                                stroke_width=stroke_width
                            ))

                            label_text = f"W{week_num} {week_start_date:%b %d}–{week_end_date:%b %d}"
                            dwg.add(dwg.text(
                                label_text,
                                insert=(label_cell_width / 2, row_y + square_size / 2 + font_size / 3),
                                font_size=font_size,
                                font_family=font_family,
                                text_anchor="middle",
                                fill="black"
                            ))

                            labeled_weeks.add(week_num)

                        # Day cell
                        dwg.add(dwg.rect(
                            insert=(col_x, row_y),
                            size=(square_size, square_size),
                            fill=cell_fill,
                            stroke=stroke_color if stroke_width > 0 else "none",
                            stroke_width=stroke_width
                        ))

                        # Optional row line at bottom of row
                        if row_line and i == 6:
                            start_x = col_x + square_size + row_line_margin_squares * square_size
                            start_y = row_y + square_size
                            end_x = start_x + row_line_length_squares * square_size
                            dwg.add(dwg.line(
                                start=(start_x, start_y),
                                end=(end_x, start_y),
                                stroke=stroke_color,
                                stroke_width=stroke_width
                            ))

    total_weeks = end_week - start_week + 1
    total_days = 7
    extra_width = (row_line_length_squares + row_line_margin_squares) * square_size if row_line else 0
    dwg['width'] = label_cell_width + total_days * square_size + extra_width
    dwg['height'] = (total_weeks + 1) * square_size  # +1 for header row

    dwg.save()
    print(f"SVG saved as {output_file} (weeks {start_week}–{end_week})")


if __name__ == "__main__":
    generate_heatmap_svg(
        year=2025,
        week_start=0,
        square_size=20,
        stroke_width=1,
        stroke_color="black",
        start_week=10,
        end_week=20,
        label_width=7.5,
        font_family="Roboto Bold",
        cell_fill="#cccccc",
        label_fill="#eeeeee",
        row_line=True,
        row_line_margin_squares=0.25,
        row_line_length_squares=1.0,
        output_file="heatmap_with_labels.svg"
    )