from typing import Any, Union, Optional

from rich.console import Console, JustifyMethod, OverflowMethod, NewLine, NO_CHANGE
from rich.style import Style


class LiveConsole(Console):
    def print_live(
            self,
            *objects: Any,
            sep: str = " ",
            end: str = "\n",
            style: Optional[Union[str, Style]] = None,
            justify: Optional[JustifyMethod] = None,
            overflow: Optional[OverflowMethod] = None,
            no_wrap: Optional[bool] = None,
            emoji: Optional[bool] = None,
            markup: Optional[bool] = None,
            highlight: Optional[bool] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            soft_wrap: Optional[bool] = None,
            new_line_start: bool = False,
    ) -> None:
        """Print to the console.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\\\\n".
            style (Union[str, Style], optional): A style to apply to output. Defaults to None.
            justify (str, optional): Justify method: "default", "left", "right", "center", or "full". Defaults to ``None``.
            overflow (str, optional): Overflow method: "ignore", "crop", "fold", or "ellipsis". Defaults to None.
            no_wrap (Optional[bool], optional): Disable word wrapping. Defaults to None.
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default. Defaults to ``None``.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default. Defaults to ``None``.
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default. Defaults to ``None``.
            width (Optional[int], optional): Width of output, or ``None`` to auto-detect. Defaults to ``None``.
            crop (Optional[bool], optional): Crop output to width of terminal. Defaults to True.
            soft_wrap (bool, optional): Enable soft wrap mode which disables word wrapping and cropping of text or ``None`` for
                Console default. Defaults to ``None``.
            new_line_start (bool, False): Insert a new line at the start if the output contains more than one line. Defaults to ``False``.
        """
        if not objects:
            objects = (NewLine(),)

        if soft_wrap is None:
            soft_wrap = self.soft_wrap
        if soft_wrap:
            if no_wrap is None:
                no_wrap = True
            if overflow is None:
                overflow = "ignore"
        render_hooks = self._render_hooks[:]
        with self:
            renderables = self._collect_renderables(
                objects,
                sep,
                end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
            for hook in render_hooks:
                renderables = hook.process_renderables(renderables)
            render_options = self.options.update(
                justify=justify,
                overflow=overflow,
                width=min(width, self.width) if width is not None else NO_CHANGE,
                height=height,
                no_wrap=no_wrap,
                markup=markup,
                highlight=highlight,
            )

            for renderable in renderables:
                sub_render_it = self.method_name()(renderable, render_options)
                for segment in sub_render_it:
                    # print("here")
                    # self._buffer.append(segment)
                    txt = self._render_buffer([segment])
                    self.file.write(txt)
                    self.file.flush()

    def method_name(self):
        render = self.render
        return render
