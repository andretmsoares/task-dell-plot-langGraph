from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .layout import generate_node_positions


C_BG = "#0d1117"; C_ACTIVE = "#00e5ff"; C_GLOW = "#1565c0"
C_IDLE = "#37474f"; C_FACE = "#161b22"; C_LABEL = "#cdd9e5"


def edge_intersection(x1, y1, x2, y2, w=0.14, h=0.09):
    dx, dy = x2 - x1, y2 - y1

    if dx == 0 and dy == 0:
        return x1, y1

    abs_dx, abs_dy = abs(dx), abs(dy)

    if abs_dx / w > abs_dy / h:
        scale = (w / 2) / abs_dx
    else:
        scale = (h / 2) / abs_dy

    return x1 + dx * scale, y1 + dy * scale


def draw_flow(
    path: List[str],
    edges: List[Tuple[str, str, str]],
    out: str,
    value: int,
    scenario: str,
    display: Dict[str, str]
) -> None:

    node_pos = generate_node_positions(edges)

    activated = set(path)
    act_edges = (
        {("__start__", path[0])}
        | {(path[i], path[i+1]) for i in range(len(path)-1)}
        | {(path[-1], "__end__")}
    )

    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-0.10, 1.25)
    ax.set_ylim(-0.08, 1.10)
    ax.axis("off")

    ax.text(
        0.50, 1.065,
        f"Plot: {scenario} - valor={value}",
        ha="center", va="center",
        fontsize=13, fontweight="bold",
        color=C_LABEL, fontfamily="monospace",
        transform=ax.transAxes
    )

    # 🔁 edges
    for src, dst, label in edges:
        xs, ys = node_pos[src]
        xd, yd = node_pos[dst]

        xs2, ys2 = edge_intersection(xs, ys, xd, yd)
        xd2, yd2 = edge_intersection(xd, yd, xs, ys)

        active = (src, dst) in act_edges

        ax.annotate(
            "",
            xy=(xd2, yd2),
            xytext=(xs2, ys2),
            arrowprops=dict(
                arrowstyle="-|>",
                color=C_ACTIVE if active else C_IDLE,
                lw=2.8 if active else 1.2,
                linestyle="solid" if active else "dashed",
                mutation_scale=50,
                alpha=1.0 if active else 0.5,
            ),
        )

        if label:
            mx, my = (xs + xd) / 2, (ys + yd) / 2
            ax.text(
                mx, my, label,
                ha="center", va="center",
                fontsize=8, fontfamily="monospace",
                color="#ffe082" if active else "#546e7a",
                bbox=dict(boxstyle="round,pad=0.18", fc=C_BG, ec="none", alpha=0.85)
            )

    # 🔲 nodes
    for node, (x, y) in node_pos.items():
        terminal = node in ("__start__", "__end__")
        active = (node in activated) or terminal

        w, h = 0.14, 0.09

        if active:
            for scale in [1.7, 1.4, 1.15]:
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x - w*scale/2, y - h*scale/2),
                    w*scale, h*scale,
                    boxstyle="round,pad=0.01",
                    fc="none", ec=C_ACTIVE,
                    lw=0.35, alpha=0.10, zorder=2
                ))

        ax.add_patch(mpatches.FancyBboxPatch(
            (x - w/2, y - h/2),
            w, h,
            boxstyle="round,pad=0.015",
            fc=C_GLOW if active else C_FACE,
            ec=C_ACTIVE if active else C_IDLE,
            lw=2.5 if active else 1.0,
            zorder=3
        ))

        ax.text(
            x, y,
            display.get(node, node),
            ha="center", va="center",
            fontsize=8.5,
            color="#ffffff" if active else "#546e7a",
            fontweight="bold",
            fontfamily="monospace",
            zorder=4,
            linespacing=1.4
        )

    patches = [
        mpatches.Patch(fc=C_GLOW, ec=C_ACTIVE, lw=2, label="No ativado"),
        mpatches.Patch(fc=C_FACE, ec=C_IDLE, lw=1.0, label="No inativo"),
        mpatches.Patch(fc=C_ACTIVE, ec=C_ACTIVE, lw=2, label="Caminho percorrido"),
        mpatches.Patch(fc=C_IDLE, ec=C_IDLE, lw=1.0, label="Caminho nao percorrido"),
    ]

    ax.legend(
        handles=patches,
        loc="lower left",
        frameon=True,
        framealpha=0.9,
        facecolor="#161b22",
        edgecolor="#37474f",
        labelcolor=C_LABEL,
        fontsize=8.5
    )

    plt.tight_layout(pad=1.4)
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

    print(f"[OK] Plot salvo -> {out}")