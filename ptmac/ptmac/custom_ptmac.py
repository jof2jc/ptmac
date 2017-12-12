# -*- coding: utf-8 -*-
# Copyright (c) 2015, jonathan and Contributors
# See license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cstr
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate
from collections import defaultdict
from frappe.model.naming import make_autoname

# test_records = frappe.get_test_records('testdoctype')

def autoname(self, method):
		# concat first and last name
		_name = " ".join(filter(None,
	 		[cstr(self.get(f)).strip().upper() for f in ["first_name", "last_name"]]))

		#self.name = cstr(self.first_name).strip() + cstr(self.last_name).strip()
		#frappe.throw(_("{0}").format(_name))

		if self.phone:
			_name = _name + ' - ' + cstr(self.phone).strip()
		elif self.mobile_no:
			_name = _name + " - " + cstr(self.mobile_no).strip()

		if frappe.db.exists("Contact", _name):
			self.name = make_autoname(_name + '/.##')
		else:
			self.name = _name

		#frappe.throw(_("{0}").format(self.name))

def item_autoname(self, method):
		if frappe.db.get_default("item_naming_by")=="Naming Series":
			if self.variant_of:
				if not self.item_code:
					template_item_name = frappe.db.get_value("Item", self.variant_of, "item_name")
					self.item_code = make_variant_item_code(self.variant_of, template_item_name, self)
			else:
				from frappe.model.naming import make_autoname
				self.item_code = make_autoname(self.naming_series+'.#####')
		elif not self.item_code:
			msgprint(_("Item Code is mandatory because Item is not automatically numbered"), raise_exception=1)

		self.item_code = self.item_code.strip().upper()
		self.item_name = self.item_code
		self.name = self.item_code

def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	conditions = []
	txt = txt.replace(" ","%")

	return frappe.db.sql("""select tabItem.name, tabItem.item_group, tabItem.image,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as decription
		from tabItem
		where tabItem.docstatus < 2
			and tabItem.has_variants=0
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and (tabItem.`{key}` LIKE %(txt)s
				or tabItem.item_group LIKE %(txt)s
				or tabItem.item_name LIKE %(txt)s
				or tabItem.description LIKE %(txt)s)
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			idx desc,
			name, item_name
		limit %(start)s, %(page_len)s """.format(key=searchfield,
			fcond=get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
			mcond=get_match_cond(doctype).replace('%', '%%')),
			{
				"today": nowdate(),
				"txt": "%%%s%%" % txt,
				"_txt": txt.replace("%", ""),
				"start": start,
				"page_len": 50
			}, as_dict=as_dict)



def set_delivery_status_per_billed(self, method):
	if self.docstatus == 1 or self.docstatus == 2:
		for d in self.items:
			if d.delivery_note:
				ref_doc_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabDelivery Note Item`
				where parent=%s""", (d.delivery_note))[0][0])
				print 'ref_doc_qty=' + cstr(ref_doc_qty)
	
				billed_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabSales Invoice Item` 
					where delivery_note=%s and docstatus=1""", (d.delivery_note))[0][0])
				print 'billed_qty=' + cstr(billed_qty)

				per_billed = ((ref_doc_qty if billed_qty > ref_doc_qty else billed_qty)\
					/ ref_doc_qty)*100
				print 'per_billed=' + cstr(per_billed)

				doc = frappe.get_doc("Delivery Note", d.delivery_note)

				#frappe.throw(_("doc.per_billed = {0} per_billed = {1}").format(doc.per_billed, per_billed))

				if self.docstatus == 1 and doc.per_billed < 100.00:
					doc.db_set("per_billed", per_billed)
				else:
					doc.db_set("per_billed", "0")

				doc.set_status(update=True)

def patch_delivery_status_per_billed():
	_list = frappe.db.sql ("""SELECT it.delivery_note, ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
			ON si.name=it.parent where si.docstatus=1 and it.delivery_note <> '' group by it.delivery_note""", as_dict=1)
	print _list

	for d in _list:
		print 'd.delivery_note=' + cstr(d.delivery_note)
		ref_doc_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabDelivery Note Item`
				where parent=%s""", (d.delivery_note))[0][0])
		print 'ref_doc_qty=' + cstr(ref_doc_qty)

		#billed_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabSales Invoice Item` 
				#where delivery_note=%s and docstatus=1""", (d.delivery_note))[0][0])
		print 'd.billed_qty=' + cstr(d.billed_qty)

		per_billed = ((ref_doc_qty if d.billed_qty > ref_doc_qty else d.billed_qty)\
				/ ref_doc_qty)*100
		print 'per_billed=' + cstr(per_billed)

		doc = frappe.get_doc("Delivery Note", d.delivery_note)

		if doc.per_billed < 100:
			doc.db_set("per_billed", per_billed)
			doc.set_status(update=True)
