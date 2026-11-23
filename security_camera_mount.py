from dataclasses import dataclass
from typing import cast

import cadquery as cq


@dataclass(frozen=True)
class SecurityCameraMount:
    """The mount for a security camera."""

    camera_radius: float = 28
    """The radius of the mount for the security camera."""

    solar_panel_radius: float = 26
    """The radius of the solar panel part of the camera."""

    bolt_diameter: float = 4.4
    """The diameter of the bolt holes to use."""

    def get_security_camera_mount(self) -> cq.Workplane:
        """Get the mount for the security camera."""
        return (
            cq.Workplane("XY")
            .cylinder(1, self.camera_radius)
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .hole(self.bolt_diameter)
        )

    def get_solar_panel_mount(self) -> cq.Workplane:
        """Get the mount for the solar panel."""
        return (
            cq.Workplane("XY")
            .cylinder(1, self.solar_panel_radius)
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .hole(self.bolt_diameter)
        )

    def get_shape(self) -> cq.Compound:
        """Get all the shapes."""
        camera_mount = self.get_security_camera_mount()
        camera_shape = cast(cq.Shape, camera_mount.val())
        camera_box = camera_shape.BoundingBox()
        solar_panel_mount = self.get_solar_panel_mount()
        solar_shape = cast(cq.Shape, solar_panel_mount.val())
        solar_box = solar_shape.BoundingBox()
        model = cq.Compound.makeCompound(
            [
                camera_shape,
                solar_shape.translate(
                    (0, (camera_box.ylen / 2) + 2 + (solar_box.ylen / 2), 0)
                ),
            ]
        )
        return model


if __name__ == "__main__":
    mount = SecurityCameraMount()
    model = mount.get_shape()
    model.export("mount.step")
