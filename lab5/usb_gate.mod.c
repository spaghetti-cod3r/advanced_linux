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
	"\x10\x00\x00\x00\xd8\x7e\x99\x92"
	"_printk\0"
	"\x14\x00\x00\x00\xe1\x88\x18\x5b"
	"dev_number\0\0"
	"\x14\x00\x00\x00\x68\x27\xf0\x77"
	"stack_class\0"
	"\x18\x00\x00\x00\x42\xc4\xff\xb8"
	"device_destroy\0\0"
	"\x18\x00\x00\x00\x91\x7d\x78\x49"
	"device_create\0\0\0"
	"\x18\x00\x00\x00\x55\xd5\xa4\xe2"
	"usb_deregister\0\0"
	"\x14\x00\x00\x00\xbb\x6d\xfb\xbd"
	"__fentry__\0\0"
	"\x1c\x00\x00\x00\xe8\x75\xa3\xef"
	"usb_register_driver\0"
	"\x1c\x00\x00\x00\xca\x39\x82\x5b"
	"__x86_return_thunk\0\0"
	"\x18\x00\x00\x00\xde\x9f\x8a\x25"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "int_stack");

MODULE_ALIAS("usb:v248Ap8367d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "BE080D820A0842BE1D6E701");
