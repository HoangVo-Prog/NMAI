def draw_graph(G, pos, path=None, out_path=None, title: str = "") -> None:
    import matplotlib.pyplot as plt
    import networkx as nx

    fig, ax = plt.subplots(figsize=(10, 8))

    # 1) Vẽ nền: cạnh mảnh, hơi trong suốt; node chưa gắn nhãn
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.4, alpha=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, linewidths=1.0)

    # 2) Tô đậm đường đi
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, width=4.0, alpha=0.9)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=path, node_size=1000,
                               linewidths=1.6, edgecolors="black")

    # 3) Edge labels có nền trắng (halo) để khỏi bị che
    edge_labels = {(u, v): f"{int(d['weight'])}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=edge_labels, font_size=8,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2),
        rotate=False
    )

    # 4) Node labels có nền trắng
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=9,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.2)
    )

    # 5) Badge số bước lệch lên trên node một chút
    if path:
        for i, node in enumerate(path):
            x, y = pos[node]
            ax.text(x, y + 10, str(i), fontsize=9, ha="center", va="bottom",
                    bbox=dict(boxstyle="circle,pad=0.25", facecolor="white",
                              edgecolor="black", alpha=0.95))

    if title:
        ax.set_title(title)
    ax.set_axis_off()
    fig.tight_layout()
    if out_path:
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)
