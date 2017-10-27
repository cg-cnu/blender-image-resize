bl_info = {
    "name": "Image Resize",
    "description": "Modify image resolution",
    "author": "Sreenivas Alapati",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "location": "UV/Image Editor > Toolshelf > Image Resize",
    "category": "Scene",
}

import bpy
import subprocess


def get_images():
    """get all the images
    """
    images = []
    # get the actual path
    for image in bpy.data.images:
        if image.source == 'FILE':
            if not image.library:
                images.append(image)
    return images


class IR_Resize_Images(bpy.types.Operator):
    """Resize Images
    """
    bl_idname = "scene.ir_resize_images"
    bl_label = "Resize Images"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scale_value = context.scene.IR_scale_value
        images = get_images()
        for image in images:
            if (context.scene.IR_scale_type == '0'):
                cmd = ['/usr/local/bin/mogrify',
                       '-resize',
                       scale_value + '%',
                       image.filepath_from_user()]
            else:
                cmd = ['/usr/local/bin/mogrify',
                       '-resize',
                       '{0}x{0}'.format(scale_value),
                       image.filepath_from_user()]

            # TODO: created by admin @ 2017-10-27 11:08:28
            # have to do a communicate and do one by one
            # launch a parallel subprocess to resize them

            # IDEA: logged by admin @ 2017-10-27 16:10:00
            # Take a backup of the image before resizing
            # restore the image back once done.

            subprocess.Popen(cmd)
            image.reload()

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        self.report({'INFO'}, 'Resized {0} images '.format(len(images)))

        return {'FINISHED'}


class Texture_Resize(bpy.types.Panel):
    """
     Resize Texutres
    """
    bl_label = "Texture Resize"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        column = layout.column(True)

        # type
        row = column.row(True)
        row.label('Type:')
        row.prop(context.scene, 'IR_scale_type')

        # value
        row = column.row(True)
        row.label('Value:')
        row.prop(context.scene, 'IR_scale_value')

        row = layout.row()
        row.operator("scene.ir_resize_images", text="Resize")

def register():
    bpy.utils.register_class(Texture_Resize)
    bpy.utils.register_class(IR_Resize_Images)
    # bpy.utils.register_module(__name__)

    scale_types = (('0', 'Percentage', ''), ('1', 'Value', ''))
    bpy.types.Scene.IR_scale_type = bpy.props.EnumProperty(
        name="",
        description="Resize Type",
        items=scale_types)
    bpy.types.Scene.IR_scale_value = bpy.props.StringProperty(
        name="",
        description="Resize Value",
        default="0")


def unregister():
    bpy.utils.unregister_class(Texture_Resize)
    del bpy.types.Scene.IR_scale_type
    del bpy.types.Scene.IR_scale_value


if __name__ == "__main__":
    register()
