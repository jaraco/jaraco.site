<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<HTML><body>
			Software Keys
			<xsl:apply-templates select="Software/Titles/Title"></xsl:apply-templates>
		</body></HTML>
	</xsl:template>
	<xsl:template match="Title">
		<a>
			<xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
			<div style="margin-top: 1em; padding: .3em; background-color: navy; color: white; font-weight: bold;">
				<xsl:value-of select="@vendor"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="text()"/> 			<xsl:text> </xsl:text>
				<xsl:value-of select="@version"/>
			</div>
		</a>
		<div style="margin-left: 5em;"><xsl:apply-templates select="//Key[@title=current()/@ID]"/></div>
	</xsl:template>
	<xsl:template match="Key">
		<div style="border: 1px solid black; background-color: #E0E0E0; margin-top:1em;"><xsl:value-of select="text()"/></div>
		<xsl:apply-templates select="@*[name()!='title']"/>
	</xsl:template>
	<xsl:template match="Key/@*">
		<div>
			<span style="font-style:italic;"><xsl:value-of select="name()"/>:</span>
			<xsl:text> </xsl:text>
			<xsl:value-of select="."/>
		</div>
	</xsl:template>
	<xsl:template match="Key/@href">
		<a>
			<xsl:attribute name="href"><xsl:value-of select="."/></xsl:attribute>
			Link
		</a>
	</xsl:template>
</xsl:stylesheet>