#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_MITIGATION_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const char ____versions[]
__used __section("__versions") =
	"\x18\x00\x00\x00\x4f\x1e\x1f\x59"
	"class_create\0\0\0\0"
	"\x14\x00\x00\x00\x69\x1b\x25\x12"
	"cdev_del\0\0\0\0"
	"\x18\x00\x00\x00\x91\x7d\x78\x49"
	"device_create\0\0\0"
	"\x18\x00\x00\x00\xbd\xb5\xbf\x6f"
	"class_destroy\0\0\0"
	"\x18\x00\x00\x00\x9f\x0c\xfb\xce"
	"__mutex_init\0\0\0\0"
	"\x10\x00\x00\x00\xd8\x7e\x99\x92"
	"_printk\0"
	"\x18\x00\x00\x00\xc2\x9c\xc4\x13"
	"_copy_from_user\0"
	"\x24\x00\x00\x00\x75\x08\x94\x89"
	"mutex_lock_interruptible\0\0\0\0"
	"\x18\x00\x00\x00\x38\xf0\x13\x32"
	"mutex_unlock\0\0\0\0"
	"\x1c\x00\x00\x00\xcb\xf6\xfd\xf0"
	"__stack_chk_fail\0\0\0\0"
	"\x18\x00\x00\x00\xe1\xbe\x10\x6b"
	"_copy_to_user\0\0\0"
	"\x10\x00\x00\x00\xba\x0c\x7a\x03"
	"kfree\0\0\0"
	"\x18\x00\x00\x00\x42\xc4\xff\xb8"
	"device_destroy\0\0"
	"\x1c\x00\x00\x00\x91\xc9\xc5\x52"
	"__kmalloc_noprof\0\0\0\0"
	"\x14\x00\x00\x00\x4b\x8d\xfa\x4d"
	"mutex_lock\0\0"
	"\x14\x00\x00\x00\xbb\x6d\xfb\xbd"
	"__fentry__\0\0"
	"\x1c\x00\x00\x00\xca\x39\x82\x5b"
	"__x86_return_thunk\0\0"
	"\x1c\x00\x00\x00\x2b\x2f\xec\xe3"
	"alloc_chrdev_region\0"
	"\x14\x00\x00\x00\x1e\x70\xe8\x75"
	"cdev_init\0\0\0"
	"\x14\x00\x00\x00\x5e\xc3\x64\xaa"
	"cdev_add\0\0\0\0"
	"\x24\x00\x00\x00\x33\xb3\x91\x60"
	"unregister_chrdev_region\0\0\0\0"
	"\x18\x00\x00\x00\xde\x9f\x8a\x25"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "AAEFD1E8B7579E0F83AB62A");
